import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

TXT_FILE = "database/oneword.txt"

# Sabhi active loops ko identify karne ke liye ek set list
active_tasks = set()

def load_txt_list():
    if not os.path.exists(TXT_FILE):
        os.makedirs(os.path.dirname(TXT_FILE), exist_ok=True)
        with open(TXT_FILE, "w", encoding="utf-8") as f:
            f.write("HELLO\nHOW\nARE\nYOU?")
    
    with open(TXT_FILE, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines() if line.strip()]

@Client.on_message(filters.command("ow", ".") & filters.me)
async def activate_loop(client, message):
    text_list = load_txt_list()
    if not text_list:
        await message.edit("<code>❌ database/oneword.txt is empty!</code>")
        return
        
    # Ek unique task ID create karenge taaki multiple loops track ho sakein
    task_id = asyncio.current_task()
    active_tasks.add(task_id)
    
    await message.edit()
    reply_to_id = message.reply_to_message.id if message.reply_to_message else None

    for item in text_list:
        # Agar saare loops force stop kar diye gaye hain toh break hoga
        if task_id not in active_tasks:
            break
        try:
            if reply_to_id:
                await client.send_message(message.chat.id, item, reply_to_message_id=reply_to_id)
            else:
                await client.send_message(message.chat.id, item)
            
            # Optimized 0.15s dynamic latency delay
            await asyncio.sleep(0.15)
            
        except FloodWait as e:
            print(f"🛑 Pyrogram FloodWait: Sleeping for {e.value}s")
            await asyncio.sleep(e.value + 1)
        except Exception:
            pass

    # Sequence khatam hote hi task saaf ho jayega
    if task_id in active_tasks:
        active_tasks.remove(task_id)

@Client.on_message(filters.command("owstop", ".") & filters.me)
async def stop_loop(client, message):
    global active_tasks
    active_tasks.clear() # Saare chal rahe loops ko ek sath crash-free stop kar dega
    await message.edit()
