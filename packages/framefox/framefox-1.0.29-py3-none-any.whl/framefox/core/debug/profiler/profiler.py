import time
import os
from typing import Dict, List, Any, Optional
import json
import uuid
from pathlib import Path
import logging
from fastapi import Request, Response


class DataCollector:
    def __init__(self, name: str, icon: str):
        self.name = name
        self.icon = icon
        self.data = {}
        
    def collect(self, request: Request, response: Response) -> None:
        pass
        
    def get_data(self) -> Dict[str, Any]:
        return self.data

class RequestDataCollector(DataCollector):
    def __init__(self):
        super().__init__("request", "fa-globe")
        
    def collect(self, request: Request, response: Response) -> None:
        self.data = {
            "method": request.method,
            "path": request.url.path,
            "path_params": dict(request.path_params),
            "query_params": dict(request.query_params),
            "headers": dict(request.headers),
            "client": request.client.host if request.client else "unknown",
            "status_code": response.status_code,
            "response_headers": dict(response.headers)
        }

class TimeDataCollector(DataCollector):
    def __init__(self):
        super().__init__("time", "fa-clock")
        self.start_time = time.time()
        
    def collect(self, request: Request, response: Response) -> None:
        end_time = time.time()
        self.data = {
            "start_time": self.start_time,
            "end_time": end_time,
            "duration": round((end_time - self.start_time) * 1000, 2)
        }

class MemoryDataCollector(DataCollector):
    def __init__(self):
        super().__init__("memory", "fa-memory")
        
    def collect(self, request: Request, response: Response) -> None:
        import psutil
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        self.data = {
            "memory_usage": memory_info.rss / (1024 * 1024),
            "peak_memory": memory_info.vms / (1024 * 1024)
        }

class SQLDataCollector(DataCollector):
    def __init__(self):
        super().__init__("database", "fa-database")
        self.queries = []
        
    def add_query(self, query: str, parameters: Dict, duration: float) -> None:
        self.queries.append({
            "query": query,
            "parameters": parameters,
            "duration": duration
        })
        
    def collect(self, request: Request, response: Response) -> None:
        self.data = {
            "queries": self.queries,
            "query_count": len(self.queries),
            "total_duration": sum(q["duration"] for q in self.queries)
        }

class RouteDataCollector(DataCollector):
    def __init__(self):
        super().__init__("route", "fa-map-signs")
        
    def collect(self, request: Request, response: Response) -> None:
        route_name = getattr(request.state, "route_name", "unknown")
        self.data = {
            "route": request.url.path,
            "route_name": route_name,
            "endpoint": str(request.scope.get("endpoint", "unknown"))
        }

class Profiler:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Profiler, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if self.initialized:
            return
            
        self.collectors = {}
        self.profiles = {}
        self.enabled = False
        self.storage_dir = Path("var/profiler")
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger("PROFILER")
        
        self.register_collector(RequestDataCollector())
        self.register_collector(TimeDataCollector())
        self.register_collector(MemoryDataCollector())
        self.register_collector(SQLDataCollector())
        self.register_collector(RouteDataCollector())
        
        self.initialized = True
    
    def enable(self) -> None:
        self.enabled = True
    
    def disable(self) -> None:
        self.enabled = False
    
    def is_enabled(self) -> bool:
        return self.enabled
    
    def register_collector(self, collector: DataCollector) -> None:
        self.collectors[collector.name] = collector
    
    def get_collector(self, name: str) -> Optional[DataCollector]:
        return self.collectors.get(name)
    
    def collect(self, request: Request, response: Response) -> str:
        if not self.enabled:
            return None
            
        token = str(uuid.uuid4())
        
        profile_data = {}
        for name, collector in self.collectors.items():
            try:
                collector.collect(request, response)
                profile_data[name] = collector.get_data()
            except Exception as e:
                self.logger.error(f"Error collecting data from {name}: {str(e)}")
        
        self.profiles[token] = profile_data
        self._save_profile(token, profile_data)
        
        return token
    
    def get_profile(self, token: str) -> Dict:
        if token in self.profiles:
            return self.profiles[token]
            
        profile_path = self.storage_dir / f"{token}.json"
        if profile_path.exists():
            with open(profile_path, 'r') as f:
                return json.load(f)
                
        return {}
    
    def _save_profile(self, token: str, data: Dict) -> None:
        try:
            profile_path = self.storage_dir / f"{token}.json"
            with open(profile_path, 'w') as f:
                json.dump(data, f, default=str)
        except Exception as e:
            self.logger.error(f"Error saving profile {token}: {str(e)}")
