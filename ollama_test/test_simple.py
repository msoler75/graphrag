#!/usr/bin/env python3
"""
Simple test script for Ollama integration with GraphRAG LLM utilities.
This script tests the JSON repair functionality and basic Ollama connectivity.
"""

import asyncio
import json
from graphrag_llm.utils.json_utils import safe_json_loads


async def test_json_repair():
    """Test the JSON repair functionality."""
    print("Testing JSON repair functionality...")

    # Test cases with malformed JSON
    test_cases = [
        '{"name": "test", "value": 123}',  # Valid JSON
        '{"name": "test", "description": "A test case"}',  # Valid JSON
        '{"name": "test", "value": 123',  # Missing closing brace
        '{"name": "test", "value": "unclosed string}',  # Unclosed string
        'Here is some text {"name": "test", "value": 123} and more text',  # JSON embedded in text
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest case {i}: {test_case[:50]}...")
        try:
            result = safe_json_loads(test_case)
            print(f"  ✓ Successfully parsed: {result}")
        except Exception as e:
            print(f"  ✗ Failed to parse: {e}")


async def test_ollama_connection():
    """Test basic connection to Ollama."""
    print("\nTesting Ollama connection...")

    try:
        from graphrag_llm.completion import create_completion
        from graphrag_llm.config import ModelConfig

        # Configure for Ollama
        config = ModelConfig(
            type="litellm",
            model_provider="ollama",
            model="llama3.2:3b",  # Use the available 3b model
            api_base="http://localhost:11434",
            api_key="dummy",  # Ollama doesn't require API key, but ModelConfig validation needs it
            max_tokens=100,
            temperature=0.0,
        )

        completion = create_completion(config)

        # Simple test prompt
        messages = [{"role": "user", "content": "Say 'Hello from Ollama!' in JSON format: {\"message\": \"Hello from Ollama!\"}"}]

        print("  Sending test request to Ollama...")
        response = await completion.completion_async(messages=messages)

        print(f"  Response received: {response.content[:100]}...")

        # Try to parse as JSON
        try:
            parsed = safe_json_loads(response.content)
            print(f"  ✓ JSON parsed successfully: {parsed}")
        except Exception as e:
            print(f"  ⚠ JSON parsing failed, but response received: {e}")

        print("  ✓ Ollama connection test completed")

    except Exception as e:
        print(f"  ✗ Ollama connection test failed: {e}")
        print("    Note: Make sure Ollama is running and the model is available")


async def main():
    """Run all tests."""
    print("🚀 Starting Ollama integration tests for GraphRAG")
    print("=" * 50)

    await test_json_repair()
    await test_ollama_connection()

    print("\n" + "=" * 50)
    print("✅ Tests completed!")
    print("\nNext steps:")
    print("1. Ensure Ollama is installed and running")
    print("2. Pull the required models: ollama pull llama3.2")
    print("3. Run the full indexing test: python test_index.py")


if __name__ == "__main__":
    asyncio.run(main())