import sys
print("Python version:", sys.version)
print("Python path:", sys.path[:3])

try:
    from groq import Groq
    print("Groq import successful")
    
    # Test direct instantiation
    client = Groq(api_key="test-key")
    print("Direct Groq() instantiation successful")
    
except Exception as e:
    print("Error:", str(e))
    print("Error type:", type(e))
