#This is a open source telegram Nmap Bot to help scan port numbers :) 
# made by iamgeo & mzz 
# contact me on telegram- iamgeo1 for any help 
# our main channel https://t.me/mzzofficial 
# Telegram to make Bot Token @BotFather 
# Use For Testing Purposes only 
# Not Responseable for what you do :) 

import os 
import subprocess
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton 

#Bot token is the numbers and Letters from BotFather Bot in telegram 
BOT_TOKEN = "YOUR BOT TOKEN" 
bot = telebot.TeleBot(BOT_TOKEN) 

#Funtion to Run Nmap Scan 
def run_nmap(target, options="-n"):
    try:
        result = subprocess.check_output(["nmap"] + options.split() + [target], stderr=subprocess.STDOUT, text=True) 
        return result
    except subprocess.CalledProcessError as e: 
        return f"X Error Running Nmap:  {e.output}"
    
# Main Menu Ui 
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("📡Scan"), KeyboardButton("⚡ Quick Scan"))
    markup.row(KeyboardButton("🔍Detailed Scan"), KeyboardButton("🌐 OS Detection"))
    markup.row(KeyboardButton("🎯Traceroute"), KeyboardButton("📖 Help"))
    markup.row(KeyboardButton("ℹ️ About"), KeyboardButton("✅ Status"))
    return markup

# Handle /help command
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "📌 **Available Commands:**\n"
        "➡️ `/start` – Start the bot & show the menu\n"
        "➡️ `/help` – Show this help message\n"
        "➡️ `/scan <IP>` – Basic Nmap scan\n"
        "➡️ `/quickscan <IP>` – Fast scan\n"
        "➡️ `/detailedscan <IP>` – Detailed scan with service detection\n"
        "➡️ `/osdetect <IP>` – Detect OS of the target\n"
        "➡️ `/traceroute <IP>` – Perform a traceroute\n"
        "➡️ `/status` – Check if the bot is running"
    )
    bot.reply_to(message, help_text, parse_mode="Markdown", reply_markup=main_menu())

    # Handle /start command
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "✅ Welcome! Choose an option below.", reply_markup=main_menu())

# Handle /status command
@bot.message_handler(commands=['status'])
def status_command(message):
    bot.reply_to(message, "✅ Bot is running and operational!")

# Generalized scan function
def perform_scan(message, scan_type, options):
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, f"⚠️ Usage: /{scan_type} <IP or domain>", reply_markup=main_menu())
        return

    target = args[1]
    bot.reply_to(message, f"🔎 Running {scan_type.replace('scan', 'Scan')} on `{target}`... Please wait.", parse_mode="Markdown")
    result = run_nmap(target, options)

    # Truncate long output to fit in Telegram messages
    if len(result) > 4000:
        result = result[:4000] + "\n...Output truncated..."

    bot.reply_to(message, f"📊 *{scan_type.replace('scan', 'Scan')} Result:*\n```\n{result}\n```", parse_mode="Markdown")

# Handle various scan commands
@bot.message_handler(commands=['scan'])
def scan_command(message):
    perform_scan(message, "Basic scan", "-n")

@bot.message_handler(commands=['quickscan'])
def quick_scan_command(message):
    perform_scan(message, "Quick scan", "-T4 -F")

@bot.message_handler(commands=['detailedscan'])
def detailed_scan_command(message):
    perform_scan(message, "Detailed scan", "-A -v")

@bot.message_handler(commands=['osdetect'])
def os_detect_command(message):
    perform_scan(message, "OS detection", "-O")

@bot.message_handler(commands=['traceroute'])
def traceroute_command(message):
    perform_scan(message, "Traceroute", "-sn --traceroute")

# Handle button presses
@bot.message_handler(func=lambda message: message.text == "📖 Help")
def help_button(message):
    help_command(message)

@bot.message_handler(func=lambda message: message.text == "📡 Scan")
def scan_button(message):
    bot.reply_to(message, "📌 Use `/scan <IP>` to start a basic scan.")

@bot.message_handler(func=lambda message: message.text == "⚡ Quick Scan")
def quick_scan_button(message):
    bot.reply_to(message, "📌 Use `/quickscan <IP>` for a fast scan.")

@bot.message_handler(func=lambda message: message.text == "🔍 Detailed Scan")
def detailed_scan_button(message):
    bot.reply_to(message, "📌 Use `/detailedscan <IP>` for a detailed scan.")

@bot.message_handler(func=lambda message: message.text == "🌐 OS Detection")
def os_detect_button(message):
    bot.reply_to(message, "📌 Use `/osdetect <IP>` to detect the target OS.")

@bot.message_handler(func=lambda message: message.text == "🎯 Traceroute")
def traceroute_button(message):
    bot.reply_to(message, "📌 Use `/traceroute <IP>` to trace the route to the target.")

@bot.message_handler(func=lambda message: message.text == "ℹ️ About")
def about_command(message):
    about_text = (
        "🤖 **Bot Information:**\n"
        "✅ This bot was created for network analysis.\n"
        "🚀 Developed by iamgeo1 & mzz\n"
        "Links to other Telegrams we own- https://t.me/BlackIceC2, https://t.me/mzzofficial Please contact us for help:)"
        "⚠️ Use responsibly and with permission!"
    )
    bot.reply_to(message, about_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "✅ Status")
def status_button(message):
    status_command(message)

# Handle unknown commands
@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    bot.reply_to(message, "❓ Unknown command. Type /help for available commands.", reply_markup=main_menu())

#start Bot 
print("Bot Is Running...")
bot.polling() 

