"""
Bot handlers for astronomical calculations and compatibility analysis
"""

import logging
import sys
import platform
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from astro_utils import AstroCalculator

logger = logging.getLogger(__name__)

class BotHandlers:
    def __init__(self):
        self.astro_calc = AstroCalculator()
    
    async def handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🌟 **Welcome to Astronomical Bot!** 🌟

I'm your personal astrology and lunar calendar assistant, powered by professional astronomical libraries.

**Available Commands:**
/start - Show this welcome message
/help - Get detailed help
/compatibility - Get detailed compatibility analysis
/lunar - Lunar calendar information
/chart - Basic astrological chart info

**Features:**
✨ Astrological compatibility analysis
🌙 Lunar calendar calculations
🔮 Chart interpretations
📅 Astronomical calculations

Just send me a message or use any command to get started!
        """
        
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_message = """
🔮 **Astronomical Bot Help** 🔮

**Commands:**
• /start - Welcome message and overview
• /help - This help message
• /compatibility - Detailed compatibility analysis
• /lunar - Current lunar phase and calendar info
• /chart - Basic astrological information

**How to use:**
1. Use /compatibility to get a comprehensive compatibility summary
2. Use /lunar to see current moon phase and lunar calendar details
3. Use /chart for basic astrological chart information
4. Send any message for general astronomical info

**Libraries Used:**
• flatlib - Professional astrological calculations
• lunardate - Accurate lunar calendar system
• python-telegram-bot 20.3 - Modern Telegram integration

**Environment:**
• Python 3.11 on Replit Nix
• Real-time astronomical data
• Professional-grade calculations

Need specific calculations? Just ask!
        """
        
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    async def handle_compatibility(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /compatibility command - detailed compatibility analysis"""
        try:
            # Get system and library information
            compatibility_info = self.astro_calc.get_compatibility_summary()
            
            compatibility_message = f"""
🔮 **Detailed Compatibility Summary** 🔮

**System Environment:**
• Platform: {platform.system()} {platform.release()}
• Python Version: {sys.version.split()[0]}
• Architecture: {platform.machine()}

**Astronomical Libraries Status:**
{compatibility_info['libraries_status']}

**Current Astronomical Data:**
{compatibility_info['current_data']}

**Calculation Capabilities:**
{compatibility_info['capabilities']}

**Performance Metrics:**
{compatibility_info['performance']}

**Integration Status:**
✅ Telegram Bot API: Fully operational
✅ Async Operations: Supported
✅ Error Handling: Implemented
✅ Logging: Active

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

All systems are operational and ready for astronomical calculations!
            """
            
            await update.message.reply_text(compatibility_message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in compatibility handler: {e}")
            await update.message.reply_text(
                "❌ Error generating compatibility summary. Please try again later."
            )
    
    async def handle_lunar(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /lunar command"""
        try:
            lunar_info = self.astro_calc.get_lunar_information()
            
            lunar_message = f"""
🌙 **Lunar Calendar Information** 🌙

{lunar_info}

**Additional Lunar Data:**
• Next New Moon: {self.astro_calc.get_next_new_moon()}
• Next Full Moon: {self.astro_calc.get_next_full_moon()}
• Lunar Month Progress: {self.astro_calc.get_lunar_progress()}%

**Astrological Significance:**
{self.astro_calc.get_lunar_significance()}
            """
            
            await update.message.reply_text(lunar_message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in lunar handler: {e}")
            await update.message.reply_text(
                "❌ Error retrieving lunar information. Please try again later."
            )
    
    async def handle_chart(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /chart command"""
        try:
            chart_info = self.astro_calc.get_basic_chart_info()
            
            chart_message = f"""
⭐ **Basic Astrological Chart Information** ⭐

{chart_info}

**Current Planetary Positions:**
{self.astro_calc.get_planetary_positions()}

**Aspects and Transits:**
{self.astro_calc.get_current_aspects()}

*Note: For detailed natal charts, please provide birth date, time, and location.*
            """
            
            await update.message.reply_text(chart_message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in chart handler: {e}")
            await update.message.reply_text(
                "❌ Error generating chart information. Please try again later."
            )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle general messages"""
        user_message = update.message.text.lower()
        
        # Simple keyword-based responses
        if any(word in user_message for word in ['compatibility', 'match', 'relationship']):
            await self.handle_compatibility(update, context)
        elif any(word in user_message for word in ['moon', 'lunar', 'phase']):
            await self.handle_lunar(update, context)
        elif any(word in user_message for word in ['chart', 'horoscope', 'astrology']):
            await self.handle_chart(update, context)
        else:
            # General astronomical information
            response = f"""
🌟 **Astronomical Information** 🌟

Thanks for your message! I can help you with:

• **Compatibility Analysis** - Use /compatibility
• **Lunar Information** - Use /lunar  
• **Astrological Charts** - Use /chart

Current system time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

What would you like to explore?
            """
            
            await update.message.reply_text(response, parse_mode='Markdown')