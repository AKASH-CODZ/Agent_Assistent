#!/usr/bin/env python3
"""
Comprehensive System Status Checker
Verifies API credentials, service availability, dependencies, and system health.
"""

import os
import sys
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from dotenv import load_dotenv

try:
    import httpx
except ImportError:
    print("❌ httpx not installed. Run: pip install httpx")
    sys.exit(1)

# Load environment variables
load_dotenv()

class StatusChecker:
    """System status checker with comprehensive reporting."""
    
    def __init__(self):
        self.results = []
        self.start_time = datetime.now()
    
    def add_result(self, category: str, name: str, status: str, message: str):
        """Add a check result."""
        self.results.append({
            "category": category,
            "name": name,
            "status": status,
            "message": message
        })
    
    async def check_groq_status(self):
        """Check Groq API status and connectivity."""
        api_key = os.getenv('GROQ_API_KEY')
        
        if not api_key:
            self.add_result("Groq API", "API Key", "❌ MISSING", "GROQ_API_KEY not set in .env")
            return
        
        if api_key == "gsk_YOUR_GROQ_API_KEY_HERE":
            self.add_result("Groq API", "API Key", "⚠️  PLACEHOLDER", "Using example key - update with real key")
            return
        
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.groq.com/openai/v1/models",
                    headers=headers,
                    timeout=10.0
                )
                
            if response.status_code == 200:
                data = response.json()
                models = [model['id'] for model in data.get('data', [])[:5]]
                self.add_result("Groq API", "Connectivity", "✅ SUCCESS", 
                              f"Connected successfully. Models: {', '.join(models)}")
            else:
                self.add_result("Groq API", "Connectivity", "❌ ERROR", 
                              f"Status {response.status_code}: {response.text[:100]}")
        except Exception as e:
            self.add_result("Groq API", "Connectivity", "❌ ERROR", str(e))
    
    async def check_pinecone_status(self):
        """Check Pinecone API status and connectivity."""
        api_key = os.getenv('PINECONE_API_KEY')
        index_name = os.getenv('PINECONE_INDEX_NAME')
        
        if not api_key:
            self.add_result("Pinecone", "API Key", "❌ MISSING", "PINECONE_API_KEY not set")
            return
        
        if api_key == "pcsk_YOUR_PINECONE_API_KEY_HERE":
            self.add_result("Pinecone", "API Key", "⚠️  PLACEHOLDER", "Using example key - update with real key")
            return
        
        if not index_name or index_name == "your_index_name_here":
            self.add_result("Pinecone", "Index Name", "⚠️  NOT CONFIGURED", "PINECONE_INDEX_NAME not set")
            return
        
        try:
            headers = {"Api-Key": api_key}
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://controller.pinecone.io/databases",
                    headers=headers,
                    timeout=10.0
                )
                
            if response.status_code == 200:
                data = response.json()
                indexes = data.get('indexes', [])
                index_exists = any(idx['name'] == index_name for idx in indexes)
                
                status = "✅ EXISTS" if index_exists else "⚠️  NOT FOUND"
                message = f"Index '{index_name}' {status.lower()}"
                
                self.add_result("Pinecone", "Index Status", status, message)
                self.add_result("Pinecone", "Available Indexes", "ℹ️  INFO", 
                              f"{len(indexes)} indexes: {', '.join([idx['name'] for idx in indexes])}")
            else:
                self.add_result("Pinecone", "Connectivity", "❌ ERROR", 
                              f"Status {response.status_code}: {response.text[:100]}")
        except Exception as e:
            self.add_result("Pinecone", "Connectivity", "❌ ERROR", str(e))
    
    def check_environment_config(self):
        """Check environment configuration."""
        app_env = os.getenv('APP_ENV', 'not set')
        debug = os.getenv('DEBUG', 'False')
        
        self.add_result("Environment", "APP_ENV", "ℹ️  INFO", app_env)
        self.add_result("Environment", "DEBUG", "ℹ️  INFO", debug)
        
        # Check if .env file exists
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            self.add_result("Configuration", ".env File", "✅ EXISTS", str(env_path))
        else:
            self.add_result("Configuration", ".env File", "⚠️  MISSING", 
                          f"Copy .env.example to .env: cp backend/.env.example backend/.env")
    
    def check_dependencies(self):
        """Check critical dependencies."""
        critical_deps = ["fastapi", "groq", "pinecone", "httpx"]
        
        for dep in critical_deps:
            try:
                __import__(dep.replace("-", "_"))
                self.add_result("Dependencies", dep, "✅ INSTALLED", "")
            except ImportError:
                self.add_result("Dependencies", dep, "❌ MISSING", "Run: pip install -r requirements.txt")
    
    def print_report(self):
        """Print comprehensive status report."""
        duration = (datetime.now() - self.start_time).total_seconds()
        
        print("\n" + "=" * 70)
        print("🔍 Akash AI Backend - System Status Report")
        print("=" * 70)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duration: {duration:.2f}s")
        print("=" * 70)
        
        # Group by category
        categories = {}
        for result in self.results:
            cat = result['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(result)
        
        for category, items in categories.items():
            print(f"\n{category}:")
            print("-" * 70)
            
            for item in items:
                icon = item['status']
                name = item['name'].ljust(15)
                msg = item['message']
                print(f"  {icon} {name}: {msg}")
        
        # Summary
        print("\n" + "=" * 70)
        total = len(self.results)
        errors = sum(1 for r in self.results if '❌' in r['status'])
        warnings = sum(1 for r in self.results if '⚠️' in r['status'])
        success = total - errors - warnings
        
        print(f"Summary: ✅ {success} OK | ⚠️  {warnings} Warnings | ❌ {errors} Errors")
        print("=" * 70)
        
        if errors > 0:
            print("\n⚠️  Action Required:")
            error_items = [r for r in self.results if '❌' in r['status']]
            for item in error_items:
                print(f"   • {item['category']} - {item['name']}: {item['message']}")
            print("\n📖 Next Steps:")
            print("   1. Check .env configuration (copy from .env.example)")
            print("   2. Verify API keys are valid and active")
            print("   3. Install dependencies: pip install -r requirements.txt")
            print("   4. Network connectivity may require VPN/proxy setup")
        
        elif warnings > 0:
            print("\n⚠️  Warnings detected - review configuration above")
        
        else:
            print("\n🎉 All systems operational!")
        
        print("=" * 70 + "\n")

async def main():
    """Main status checker."""
    print("\n🚀 Starting System Status Check...\n")
    
    checker = StatusChecker()
    
    # Run checks
    checker.check_environment_config()
    checker.check_dependencies()
    await checker.check_groq_status()
    await checker.check_pinecone_status()
    
    # Print report
    checker.print_report()
    
    # Exit with appropriate code
    errors = sum(1 for r in checker.results if '❌' in r['status'])
    sys.exit(1 if errors > 0 else 0)

if __name__ == "__main__":
    asyncio.run(main())
