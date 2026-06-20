import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

TXT_FILE = "database/text_raid.txt"
active_raid_tasks = set()

def load_txt_list():
    if not os.path.exists(TXT_FILE):
        os.makedirs(os.path.dirname(TXT_FILE), exist_ok=True)
        with open(TXT_FILE, "w", encoding="utf-8") as f:
            f.write("Raid Line 1\nRaid Line 2")
            
    with open(TXT_FILE, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines() if line.strip()]

@Client.on_message(filters.command("at", ".") & filters.me)
async def activate_raid(client, message):
    text_list = load_txt_list()
    if not text_list:
        await message.edit("<code>❌ database/text_raid.txt is empty!</code>")
        return
        
    task_id = asyncio.current_task()
    active_raid_tasks.add(task_id)
    
    await message.edit()
    reply_to_id = message.reply_to_message.id if message.reply_to_message else None

    for item in text_list:
        if task_id not in active_raid_tasks:
            break
        try:
            if reply_to_id:
                await client.send_message(message.chat.id, item, reply_to_message_id=reply_to_id)
            else:
                await client.send_message(message.chat.id, item)
                
            await asyncio.sleep(0.15)
            
        except FloodWait as e:
            print(f"🛑 Pyrogram FloodWait: Sleeping for {e.value}s")
            await asyncio.sleep(e.value + 1)
        except Exception:
            pass
            
    if task_id in active_raid_tasks:
        active_raid_tasks.remove(task_id)

@Client.on_message(filters.command("atstop", ".") & filters.me)
async def stop_raid(client, message):
    global active_raid_tasks
    active_raid_tasks.clear()
    await message.edit()
