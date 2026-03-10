import os
import sys

# Clear any proxy environment variables
for key in list(os.environ.keys()):
    if 'proxy' in key.lower():
        del os.environ[key]

# Remove current directory from path temporarily
current_dir = os.getcwd()
if current_dir in sys.path:
    sys.path.remove(current_dir)

print("Testing isolated Groq client...")
try:
    from groq import Groq
    client = Groq(api_key="test")
    print("SUCCESS: Isolated Groq client works!")
except Exception as e:
    print(f"FAILED: {e}")
    print(f"Error type: {type(e)}")
    
    # Try to get more details about the error
    import traceback
    traceback.print_exc()
