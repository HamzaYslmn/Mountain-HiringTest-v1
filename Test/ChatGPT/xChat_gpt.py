import asyncio
import os
from datetime import datetime

async def process_user_input(userinput: str, thread_id: str, assistant_id: str):
    try:
        if not userinput or not thread_id or not assistant_id:
            streamtext = "ERR! Missing required parameters."
            yield streamtext, None, datetime.now(), None

        full_text = "Hello, I am a GPT-1 chatbot. I am here to assist you. How can I help you today?"
        my_thread = "thrd_123456" 
        
        yield full_text, my_thread, datetime.now(), None

    except Exception as e:
        yield None, None, datetime.now(), str(e)

    finally:
        return

async def main():
    userinput = "Hello"
    thread_id = "123"
    assistant_id = "456"

    # Asynchronously stream the output in chunks
    async for streamtext, my_thread, timestamp, error in process_user_input(userinput, thread_id, assistant_id):
        if error:
            print(f"Error occurred at {timestamp}: {error}")
        else:
            print(f"[{timestamp}] ({my_thread}): {streamtext}")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
