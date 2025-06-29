#!/usr/bin/env python3
"""
Telegram Bot with Astronomical Libraries
Entry point for the bot running on Replit's Nix environment
"""

import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from bot_handlers import BotHandlers

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class AstronomicalBot:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN", "your_bot_token_here")
        self.handlers = BotHandlers()
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command"""
        await self.handlers.handle_start(update, context)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /help command"""
        await self.handlers.handle_help(update, context)
    
    async def compatibility_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /compatibility command"""
        await self.handlers.handle_compatibility(update, context)
    
    async def lunar_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /lunar command"""
        await self.handlers.handle_lunar(update, context)
    
    async def chart_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /chart command"""
        await self.handlers.handle_chart(update, context)
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Log errors caused by Updates"""
        logger.error(f"Exception while handling an update: {context.error}")
        
        if isinstance(update, Update) and update.effective_message:
            await update.effective_message.reply_text(
                "Sorry, an error occurred while processing your request. Please try again later."
            )
    
    def setup_handlers(self, application):
        """Set up command and message handlers"""
        # Command handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("compatibility", self.compatibility_command))
        application.add_handler(CommandHandler("lunar", self.lunar_command))
        application.add_handler(CommandHandler("chart", self.chart_command))
        
        # Message handler for non-command messages
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.handle_message))
        
        # Error handler
        application.add_error_handler(self.error_handler)
    
    async def run(self):
        """Main bot execution"""
        logger.info("Starting Astronomical Telegram Bot...")
        
        # Validate token
        if self.token == "your_bot_token_here":
            logger.error("Please set the TELEGRAM_BOT_TOKEN environment variable!")
            return
        
        # Create application
        application = Application.builder().token(self.token).build()
        
        # Setup handlers
        self.setup_handlers(application)
        
        # Start the bot
        logger.info("Bot is starting...")
        await application.run_polling(allowed_updates=Update.ALL_TYPES)

async def main():
    """Main entry point"""
    bot = AstronomicalBot()
    await bot.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")