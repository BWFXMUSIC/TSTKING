import time
import requests
from L2RMUSIC import app
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters

API_URL = "https://chatgpt.apinepdev.workers.dev/?question="  # Ensure this API is working

@app.on_message(filters.command(["chatgpt", "ai", "ask", "gpt", "solve"], prefixes=["+", ".", "/", "-", "", "$", "#", "&"]))
async def chat_gpt(bot, message):
    try:
        start_time = time.time()
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            return await message.reply_text("Example:\n\n`/chatgpt Where is the Taj Mahal?`", parse_mode=ParseMode.MARKDOWN)

        question = message.text.split(' ', 1)[1]
        response = requests.get(f"{API_URL}{question}")

        if response.status_code == 200:
            json_data = response.json()

            if "answer" in json_data:
                answer = json_data["answer"]
                end_time = time.time()
                response_time = round((end_time - start_time) * 1000, 3)

                return await message.reply_text(
                    f"**🤖 ChatGPT Response:**\n\n{answer}\n\n⏳ Response Time: `{response_time} ms`\n\n_Answered by https://t.me/ALL_QUIZ_TAME",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                return await message.reply_text("⚠️ No valid answer found in the response.")
        else:
            return await message.reply_text(f"⚠️ API Error: Received status code {response.status_code}")

    except Exception as e:
        return await message.reply_text(f"⚠️ **Error:** `{str(e)}`", parse_mode=ParseMode.MARKDOWN)
