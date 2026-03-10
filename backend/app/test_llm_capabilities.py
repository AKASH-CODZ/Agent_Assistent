#!/usr/bin/env python3
"""
LLM Capabilities Testing Script
Tests various aspects of the Groq LLM integration with different scenarios.
"""

import requests
import json
import time
from typing import Dict, Any, List

BASE_URL = "http://127.0.0.1:8001"

def test_basic_conversation():
    """Test basic conversational capabilities."""
    print("🤖 Testing Basic Conversation...")
    payload = {
        "message": "Hello! Can you tell me about yourself?",
        "user_type": "visitor"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/chat",
        headers={"Content-Type": "application/json"},
        json=payload
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Response: {data['reply'][:100]}...")
        print(f"📝 Context Items: {len(data['context_used'])}")
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False

def test_technical_depth():
    """Test technical depth and developer-focused responses."""
    print("\n💻 Testing Technical Depth...")
    payload = {
        "message": "Explain the architecture of your AI assistant backend in detail",
        "user_type": "developer"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/chat",
        headers={"Content-Type": "application/json"},
        json=payload
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Technical Response Generated")
        print(f"📏 Response Length: {len(data['reply'])} characters")
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False

def test_professional_context():
    """Test recruiter/professional context responses."""
    print("\n👔 Testing Professional Context...")
    payload = {
        "message": "What makes you stand out as a software engineer?",
        "user_type": "recruiter"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/chat",
        headers={"Content-Type": "application/json"},
        json=payload
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Professional Response Generated")
        print(f"🎯 Key Points Covered: {[ctx[:50] for ctx in data['context_used']]}")
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False

def test_context_relevance():
    """Test how well the system uses context."""
    print("\n🔍 Testing Context Relevance...")
    
    test_cases = [
        {
            "query": "Tell me about your trading platform",
            "expected_category": "trading"
        },
        {
            "query": "What web development experience do you have?",
            "expected_category": "web-development"
        },
        {
            "query": "Describe your AI and machine learning projects",
            "expected_category": "ai-ml"
        }
    ]
    
    results = []
    for i, case in enumerate(test_cases):
        payload = {
            "message": case["query"],
            "user_type": "visitor"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/chat",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            # Check if context contains expected category
            context_text = " ".join(data['context_used']).lower()
            has_expected = case["expected_category"] in context_text
            results.append(has_expected)
            print(f"  Test {i+1}: {'✅' if has_expected else '❌'} - {case['query']}")
        else:
            print(f"  Test {i+1}: ❌ Error")
            results.append(False)
        
        time.sleep(0.5)  # Small delay between requests
    
    success_rate = sum(results) / len(results) * 100
    print(f"\n📊 Context Relevance Success Rate: {success_rate:.1f}%")
    return success_rate >= 60

def test_response_consistency():
    """Test consistency of responses across similar queries."""
    print("\n🔄 Testing Response Consistency...")
    
    similar_queries = [
        "What programming languages do you know?",
        "Tell me about your technical skills",
        "What are your coding abilities?"
    ]
    
    responses = []
    for query in similar_queries:
        payload = {
            "message": query,
            "user_type": "recruiter"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/chat",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            responses.append({
                "query": query,
                "response_length": len(data['reply']),
                "first_sentence": data['reply'].split('.')[0] if '.' in data['reply'] else data['reply'][:50]
            })
        time.sleep(0.5)
    
    print("Consistency Analysis:")
    for resp in responses:
        print(f"  Query: {resp['query']}")
        print(f"  Length: {resp['response_length']} chars")
        print(f"  Opening: {resp['first_sentence']}...")
        print()
    
    return len(responses) == len(similar_queries)

def test_error_handling():
    """Test error handling and edge cases."""
    print("\n🛡️ Testing Error Handling...")
    
    # Test malformed request
    response = requests.post(
        f"{BASE_URL}/api/v1/chat",
        headers={"Content-Type": "application/json"},
        json={}  # Empty payload
    )
    
    if response.status_code == 422:
        print("✅ Validation error handled correctly")
        return True
    else:
        print(f"❌ Unexpected response: {response.status_code}")
        return False

def test_service_health():
    """Test overall service health."""
    print("\n🏥 Testing Service Health...")
    
    response = requests.get(f"{BASE_URL}/api/v1/")
    
    if response.status_code == 200:
        data = response.json()
        services = data.get('services', {})
        print(f"Services Status:")
        for service, status in services.items():
            print(f"  {service}: {'✅ Active' if status else '⚠️  Mock Mode'}")
        return True
    else:
        print(f"❌ Health check failed")
        return False

def main():
    """Run all LLM capability tests."""
    print("🚀 LLM Capabilities Test Suite")
    print("=" * 50)
    
    try:
        tests = [
            ("Service Health", test_service_health),
            ("Basic Conversation", test_basic_conversation),
            ("Technical Depth", test_technical_depth),
            ("Professional Context", test_professional_context),
            ("Context Relevance", test_context_relevance),
            ("Response Consistency", test_response_consistency),
            ("Error Handling", test_error_handling)
        ]
        
        results = []
        for test_name, test_func in tests:
            print(f"\n🧪 {test_name}")
            print("-" * 30)
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ Test failed with exception: {str(e)}")
                results.append((test_name, False))
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 50)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print(f"\n📈 Overall Score: {passed}/{total} ({(passed/total)*100:.1f}%)")
        
        if passed == total:
            print("🎉 All tests passed! The LLM integration is working perfectly.")
        elif passed >= total * 0.8:
            print("👍 Good performance! Most capabilities are working well.")
        else:
            print("⚠️  Some issues detected. Review the failing tests above.")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the server is running.")
        print("Start the server with: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Test suite failed with error: {str(e)}")

if __name__ == "__main__":
    main()