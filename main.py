from telethon import TelegramClient, events
import asyncio
import os
import re
from telegram import Bot
from telegram.constants import ParseMode
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
source_channel = os.getenv('SOURCE_CHANNEL')  # without @
target_channel = os.getenv('TARGET_CHANNEL')  # with @
bot_token = os.getenv('BOT_TOKEN')

# Telegram Clients
client = TelegramClient('session_name', api_id, api_hash)
bot = Bot(token=bot_token)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    try:
        original_text = event.message.message
        if original_text:
            print("New message received:", original_text)
            #print("RAW TEXT:\n", repr(original_text))

            # Extract values using regex
            pair_match = re.search(r'([A-Z]+)/([A-Z]+)', original_text)
            direction = re.search(r'Sinyal\s+Y[oö]n[üu]\s*=\s*(LONG|SHORT)', original_text, re.IGNORECASE)
            entry = re.search(r'Giri[sş]\s*=\s*\[\s*([0-9.]+)\s*Arasında\s*([0-9.]+)\s*\]', original_text, re.IGNORECASE)
            leverage = re.search(r'Kald[ıi]ra[çc]\s*[:\-–]?\s*-?\s*([0-9a-zA-ZxX]+)', original_text, re.IGNORECASE)
            stop = re.search(r'StopLoss\s*[:\-–]?\s*-?\s*([0-9.]+)', original_text, re.IGNORECASE)
            targets = re.search(r'Kar\s+Hedeflerimiz\s*=\s*\[([^\]]+)\]', original_text, re.IGNORECASE)

            #print(leverage)
            #print(entry)
            #print(stop)
            
            # Parse values
            pair = f"{pair_match.group(1).capitalize()} / {pair_match.group(2)}" if pair_match else "Pair / USDT"
            direction_text = direction.group(1).upper() if direction else "LONG"
            leverage_text = leverage.group(1).strip() if leverage else "-"
            entry_text = f"{entry.group(1).strip()} {entry.group(2).strip()}" if entry else "-"
            stop_text = stop.group(1).strip() if stop else "-"
            targets_list = [t.strip() for t in targets.group(1).split(",")] if targets else []
            #print(pair)
            #print(direction_text)
            #print(leverage_text)
            #print(entry_text)
            #print(stop_text)
            #print(targets_list)

            # Format direction line with emojis
            if direction_text == "LONG":
                direction_line = f"🟢 {direction_text} / {leverage_text}"
            elif direction_text == "SHORT":
                direction_line = f"🔴 {direction_text} / {leverage_text}"
            else:
                direction_line = f"{direction_text} / {leverage_text}"

            # Format targets
            formatted_targets = "\n".join(targets_list)

            # Compose final message
            final_message = f"""💸 {pair}

{direction_line}

✅ GİRİŞ: [{entry_text}]

🔴 STOP: {stop_text}

🚀 HƏDƏFLƏR
{formatted_targets}

#Yatirim tovsiyyesi deyil!"""

            # Send it
            await bot.send_message(chat_id=target_channel, text=final_message, parse_mode=ParseMode.HTML)

    except Exception as e:
        print("Error:", e)

async def main():
    await client.start(bot_token=bot_token)
    print("Bot is now running...")
    await client.run_until_disconnected()

asyncio.run(main())
