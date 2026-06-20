import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from utils.misc import add_module_info

TXT_FILE = "database/oneword.txt"
active_tasks = set()

def load_txt_list():
    if not os.path.exists(TXT_FILE):
        os.makedirs(os.path.dirname(TXT_FILE), exist_ok=True)
        # Empty file create karega bina kisi dummy text ke
        with open(TXT_FILE, "w", encoding="utf-8") as f:
            pass
    
    with open(TXT_FILE, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines() if line.strip()]

@Client.on_message(filters.command("ow", ".") & filters.me)
async def activate_loop(client, message):
    text_list = load_txt_list()
    if not text_list:
        await message.edit("<code>❌ database/oneword.txt is empty!</code>")
        return
        
    task_id = asyncio.current_task()
    active_tasks.add(task_id)
    
    await message.delete() # Trigger hote hi command message delete ho jayega, koi extra text nahi rahega
    reply_to_id = message.reply_to_message.id if message.reply_to_message else None

    for item in text_list:
        if task_id not in active_tasks:
            break
        try:
            if reply_to_id:
                await client.send_message(message.chat.id, item, reply_to_message_id=reply_to_id)
            else:
                await client.send_message(message.chat.id, item)
            
            await asyncio.sleep(0.15)
            
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
        except Exception:
            pass

    if task_id in active_tasks:
        active_tasks.remove(task_id)

@Client.on_message(filters.command("owstop", ".") & filters.me)
async def stop_loop(client, message):
    global active_tasks
    active_tasks.clear() 
    await message.delete() # Koi confirmation text nahi bhejega, silently sab stop kar dega

add_module_info(
    module_name="oneword",
    commands={
        ".ow": "Run words sequence from database/oneword.txt",
        ".owstop": "Force Stop all active running word sequences instantly"
    }
)
