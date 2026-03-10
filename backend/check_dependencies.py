#!/usr/bin/env python3
"""
Dependency Status Checker
Verifies all required packages are installed and imports correctly.
"""

import sys
import importlib
from typing import Dict, List, Tuple

# Define required dependencies with minimum versions
REQUIRED_PACKAGES = {
    "fastapi": ("fastapi", "0.100.0"),
    "uvicorn": ("uvicorn", "0.24.0"),
    "groq": ("groq", "0.5.0"),
    "pinecone": ("pinecone", "3.0.0"),
    "sentence_transformers": ("sentence-transformers", "2.2.0"),
    "torch": ("torch", "2.0.0"),
    "transformers": ("transformers", "4.35.0"),
    "python_dotenv": ("python-dotenv", "1.0.0"),
    "pydantic": ("pydantic", "2.5.0"),
    "httpx": ("httpx", "0.25.0"),
    "pytest": ("pytest", "7.4.0"),
}

def get_package_version(package_name: str) -> str:
    """Get installed version of a package."""
    try:
        module = importlib.import_module(package_name)
        return getattr(module, "__version__", "unknown")
    except ImportError:
        return "NOT INSTALLED"

def check_dependencies() -> Tuple[List[Dict], List[Dict]]:
    """Check all dependencies and return (installed, missing) lists."""
    installed = []
    missing = []
    
    print("🔍 Checking Dependencies...\n")
    
    for import_name, (package_name, min_version) in REQUIRED_PACKAGES.items():
        version = get_package_version(import_name)
        
        if version == "NOT INSTALLED":
            missing.append({
                "package": package_name,
                "required": min_version,
                "installed": version
            })
        else:
            installed.append({
                "package": package_name,
                "required": min_version,
                "installed": version
            })
    
    return installed, missing

def print_status(installed: List[Dict], missing: List[Dict]):
    """Print dependency status report."""
    print("=" * 60)
    
    if installed:
        print("✅ Installed Packages:")
        for pkg in installed:
            print(f"   ✓ {pkg['package']}: {pkg['installed']}")
        print()
    
    if missing:
        print("❌ Missing Packages:")
        for pkg in missing:
            print(f"   ✗ {pkg['package']}: Required {pkg['required']} - NOT INSTALLED")
        print()
    
    print("-" * 60)
    total = len(installed) + len(missing)
    print(f"Summary: {len(installed)}/{total} packages installed")
    
    if missing:
        print("\n⚠️  Action Required:")
        print("   Run: pip install -r requirements.txt")
        print(f"   Missing: {', '.join([p['package'] for p in missing])}")
    else:
        print("\n🎉 All dependencies are installed!")
    
    print("=" * 60)

def main():
    """Main dependency checker."""
    installed, missing = check_dependencies()
    print_status(installed, missing)
    
    # Exit with error code if any packages are missing
    sys.exit(1 if missing else 0)

if __name__ == "__main__":
    main()
