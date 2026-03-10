"""Monitoring and health check utilities."""

import psutil
import time
from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class SystemMonitor:
    """System resource monitoring utility."""
    
    @staticmethod
    def get_system_resources() -> Dict[str, float]:
        """Get current system resource usage."""
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent,
                "uptime_seconds": time.time() - psutil.boot_time()
            }
        except Exception as e:
            logger.error(f"Error getting system resources: {e}")
            return {}

    @staticmethod
    def get_process_info() -> Dict[str, Any]:
        """Get current process information."""
        try:
            process = psutil.Process()
            return {
                "pid": process.pid,
                "memory_mb": process.memory_info().rss / 1024 / 1024,
                "cpu_percent": process.cpu_percent(),
                "threads": process.num_threads(),
                "open_files": len(process.open_files()) if hasattr(process, 'open_files') else 0
            }
        except Exception as e:
            logger.error(f"Error getting process info: {e}")
            return {}


class HealthChecker:
    """Comprehensive health checking utility."""
    
    def __init__(self):
        self.start_time = time.time()
    
    def get_uptime(self) -> float:
        """Get application uptime in seconds."""
        return time.time() - self.start_time
    
    async def check_service_health(self, service_name: str, health_check_func) -> Dict[str, Any]:
        """Perform health check on a service."""
        start_time = time.time()
        try:
            result = await health_check_func()
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            return {
                "status": "healthy" if result.get("status") == "success" else "unhealthy",
                "response_time_ms": round(response_time, 2),
                "timestamp": datetime.now().isoformat(),
                "details": {
                    "error_message": result.get("error"),
                    "version": result.get("version", "unknown")
                }
            }
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            logger.error(f"Health check failed for {service_name}: {e}")
            return {
                "status": "unhealthy",
                "response_time_ms": round(response_time, 2),
                "timestamp": datetime.now().isoformat(),
                "details": {
                    "error_message": str(e),
                    "version": "unknown"
                }
            }
    
    def get_overall_status(self, services_status: Dict[str, Dict]) -> str:
        """Determine overall system status based on service statuses."""
        unhealthy_count = sum(1 for service in services_status.values() 
                            if service["status"] == "unhealthy")
        degraded_count = sum(1 for service in services_status.values() 
                           if service["status"] == "degraded")
        
        if unhealthy_count > 0:
            return "unhealthy"
        elif degraded_count > 0:
            return "degraded"
        else:
            return "healthy"


# Global instances
system_monitor = SystemMonitor()
health_checker = HealthChecker()