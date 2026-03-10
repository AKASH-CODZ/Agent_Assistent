#!/usr/bin/env python3
"""
LLM Response Comparison Demo
Shows the difference between mock and real LLM responses.
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8001"

def get_current_status():
    """Get current service status."""
    response = requests.get(f"{BASE_URL}/api/v1/")
    if response.status_code == 200:
        return response.json().get('services', {})
    return {}

def demo_query(query, user_type="visitor"):
    """Demo a single query and show detailed response info."""
    print(f"\n📝 Query: '{query}' (as {user_type})")
    print("-" * 60)
    
    payload = {
        "message": query,
        "user_type": user_type
    }
    
    start_time = datetime.now()
    response = requests.post(
        f"{BASE_URL}/api/v1/chat",
        headers={"Content-Type": "application/json"},
        json=payload
    )
    end_time = datetime.now()
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"⏱️  Response Time: {(end_time - start_time).total_seconds():.2f}s")
        print(f"🔤 Response Length: {len(data['reply'])} characters")
        print(f"📚 Context Items: {len(data['context_used'])}")
        print(f"👤 User Type: {data['user_type']}")
        print(f"\n🤖 Response Preview:")
        print(f"{data['reply'][:300]}{'...' if len(data['reply']) > 300 else ''}")
        
        print(f"\n📋 Context Used:")
        for i, context in enumerate(data['context_used'][:2], 1):
            print(f"  {i}. {context[:100]}...")
        
        return True
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return False

def main():
    """Run LLM comparison demo."""
    print("🤖 LLM Response Comparison Demo")
    print("=" * 60)
    
    # Show current status
    status = get_current_status()
    print("🔌 Current Service Status:")
    for service, active in status.items():
        print(f"  {service}: {'🟢 Active' if active else '🟡 Mock Mode'}")
    
    print("\n" + "=" * 60)
    print(" демо Conversations")
    print("=" * 60)
    
    # Test different scenarios
    test_cases = [
        {
            "query": "Tell me about your trading platform project",
            "user_type": "developer",
            "description": "Technical deep-dive query"
        },
        {
            "query": "What makes you a strong candidate for this role?",
            "user_type": "recruiter", 
            "description": "Professional positioning query"
        },
        {
            "query": "Can you explain what you do in simple terms?",
            "user_type": "visitor",
            "description": "General audience query"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n🚀 Test Case {i}: {case['description']}")
        success = demo_query(case['query'], case['user_type'])
        if not success:
            break
    
    print("\n" + "=" * 60)
    print("💡 Key Differences to Expect:")
    print("=" * 60)
    print("🟡 MOCK MODE (Current):")
    print("   • Template-based responses")
    print("   • Pre-defined content patterns") 
    print("   • Fixed response structures")
    print("   • No real language understanding")
    
    print("\n🟢 REAL LLM (With API Keys):")
    print("   • Natural, conversational responses")
    print("   • Context-aware answer generation")
    print("   • Dynamic content creation")
    print("   • Personalized tone adjustment")
    print("   • Better handling of complex queries")
    
    print("\n📋 Next Steps:")
    print("1. Get free API keys from Groq and Pinecone")
    print("2. Update your .env file with real credentials")
    print("3. Restart the server")
    print("4. Run this demo again to see the difference!")
    
    print("\n📖 See API_SETUP_GUIDE.md for detailed setup instructions")

if __name__ == "__main__":
    main()