import httpx
import asyncio
import base64
import json
import os

# Base URL for your API
BASE_URL = "http://localhost:8001/AI"

async def test_root_endpoint():
    """Test the root endpoint"""
    print("🧪 Testing Root Endpoint...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/status")
            print(f"Root Status: {response.status_code}")
            print(f"Root Response: {response.text}")
        except Exception as e:
            print(f"❌ Root test failed: {e}")
    print("-" * 50)

async def test_chat_endpoint() -> None:
    """Exercise /openai/chat and print the streamed response live."""
    print("🧪  Testing Chat Endpoint …")

    headers = {
        "Authorization": "Mountain",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "message": "Hello, how can you help me with Mountain AI projects?",
        "agent_id": "pmpt_6867eb8b4fc08195929708cbd183ca420d2cf33d36b5ace3",
    }

    try:
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{BASE_URL}/openai/chat",
                json=payload,
                headers=headers,
                timeout=30.0,
            ) as resp:
                print(f"Status → {resp.status_code}")
                resp.raise_for_status()

                print("🌀  Streaming:")
                full_bytes = bytearray()
                async for chunk in resp.aiter_bytes():
                    print(chunk.decode("utf-8", errors="ignore"), end="", flush=True)
                    full_bytes.extend(chunk)

        print(f"\n✅  Stream complete. ({len(full_bytes)} bytes)")
        try:
            parsed = json.loads(full_bytes.decode("utf-8", errors="ignore"))
            print(json.dumps(parsed, indent=2, ensure_ascii=False))
        except json.JSONDecodeError as err:
            print("⚠️  Final payload is not valid JSON:", err)
    except httpx.HTTPError as e:
        print(f"❌  HTTP error during chat test: {e}")

async def test_chat_with_image():
    """Test chat endpoint with base64 image"""
    print("🧪 Testing Chat with Image...")
    
    # Try to read cat.jpg and convert to base64
    try:
        image_path = "cat.jpg"
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                img_data = img_file.read()
                img_base64 = base64.b64encode(img_data).decode('utf-8')
                img_data_url = f"data:image/jpeg;base64,{img_base64}"
                print(f"✅ Found cat.jpg, size: {len(img_data)} bytes")
        else:
            # Create a simple test base64 image if cat.jpg doesn't exist
            print("⚠️ cat.jpg not found, using placeholder base64")
            img_data_url = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwA/wA/QA="
        
        async with httpx.AsyncClient() as client:
            chat_data = {
                "message": "Can you describe what you see in this image?",
                "agent_id": "pmpt_6867eb8b4fc08195929708cbd183ca420d2cf33d36b5ace3",
                "photo": img_data_url
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Mountain"
            }
            
            response = await client.post(
                f"{BASE_URL}/openai/chat",
                json=chat_data,
                headers=headers,
                timeout=30.0
            )
            print(f"Chat with Image Status: {response.status_code}")
            
            if response.status_code == 200:
                print("Chat with Image Response:")
                content = response.text
                print(content[:200] + "..." if len(content) > 200 else content)
            else:
                print(f"Chat with Image Error: {response.text}")
                
    except Exception as e:
        print(f"❌ Chat with image test failed: {e}")
    print("-" * 50)

async def test_stt_endpoint():
    """Test the Speech-to-Text endpoint"""
    print("🧪 Testing STT Endpoint...")
    
    try:
        # Try to read Pickle_Rick.wav and convert to base64
        audio_path = "Pickle_Rick.wav"
        if os.path.exists(audio_path):
            with open(audio_path, "rb") as audio_file:
                audio_data = audio_file.read()
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                print(f"✅ Found Pickle_Rick.wav, size: {len(audio_data)} bytes")
        else:
            print("⚠️ Pickle_Rick.wav not found, using placeholder audio data")
            # Create minimal WAV header for testing
            audio_base64 = "UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA="
        
        async with httpx.AsyncClient() as client:
            stt_data = {
                "audio": audio_base64,
                "thread_id": "test-thread-123",
                "assistant_id": "test-assistant-123"
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Mountain"
            }
            
            response = await client.post(
                f"{BASE_URL}/openai/stt",
                json=stt_data,
                headers=headers,
                timeout=30.0
            )
            print(f"STT Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"STT Response: {result}")
            else:
                print(f"STT Error: {response.text}")
                
    except Exception as e:
        print(f"❌ STT test failed: {e}")
    print("-" * 50)

async def test_tts_endpoint():
    """Test the Text-to-Speech endpoint"""
    print("🧪 Testing TTS Endpoint...")
    
    async with httpx.AsyncClient() as client:
        tts_data = {
            "text": "Hello, this is a test of the text to speech functionality from Mountain AI.",
            "thread_id": "test-thread-123",
            "assistant_id": "test-assistant-123"
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Mountain"
        }
        
        try:
            response = await client.post(
                f"{BASE_URL}/openai/tts",
                json=tts_data,
                headers=headers,
                timeout=30.0
            )
            print(f"TTS Status: {response.status_code}")
            
            if response.status_code == 200:
                # Save the audio response to a file
                with open("test_output.wav", "wb") as f:
                    f.write(response.content)
                print(f"TTS Response: Audio saved to test_output.wav ({len(response.content)} bytes)")
            else:
                print(f"TTS Error: {response.text}")
                
        except Exception as e:
            print(f"❌ TTS test failed: {e}")
    print("-" * 50)

async def main():
    """Run all tests"""
    print("🚀 Starting API Tests for Mountain AI Backend")
    print("=" * 60)
    
    await test_root_endpoint()
    await test_chat_endpoint()
    await test_chat_with_image()
    await test_stt_endpoint()
    await test_tts_endpoint()
    
    print("✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())