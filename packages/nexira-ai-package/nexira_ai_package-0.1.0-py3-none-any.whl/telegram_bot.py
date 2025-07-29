import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
import httpx

class NexiraBot:
    def __init__(self, bot_token: str, api_url: str):
        self.api_url = api_url
        self.application = ApplicationBuilder().token(bot_token).build()
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🤖 Hello! I'm your LLM chatbot. Send me a message!")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_input = update.message.text
        try:
            print(f"Received message: {user_input}")
            url = self.api_url + "/llm_model/ask"
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, json={'question': user_input})
                print(f"Response: {response}")
                print(f"Response content: {response.json()}")
                await update.message.reply_text(response.json()['response'])
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    
    def run(self):
        print("🤖 Bot is running...")
        self.application.run_polling()
