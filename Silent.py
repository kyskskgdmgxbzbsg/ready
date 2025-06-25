import asyncio
import logging
import requests
import os
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ========== CONFIG ==============

BOT_TOKEN = "7983426072:AAET5i3wk_-xmG7QBms9x9X8o2wdJeYODQQ"
BOT_USERNAME = "RDX_Hacker"
CHANNEL_USERNAME = "https://t.me/CrazyEarning_x"

# ================================

logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("telegram").setLevel(logging.CRITICAL)
logging.getLogger("apscheduler").setLevel(logging.CRITICAL)
logging.basicConfig(level=logging.CRITICAL)

EMOJIS = {
    "mobile": "📱",
    "name": "👤",
    "fname": "👨‍👦",
    "address": "📍",
    "alt": "☎️",
    "circle": "🗽️",
    "id": "🆔",
    "VehicleNumber": "🚘",
    "OwnerName": "👤",
    "FatherName": "👨‍👦",
    "PermanentAddress": "🏠",
    "RegistrationDate": "📆",
    "MakerModel": "🔧",
    "Fuel": "⛽",
    "Color": "🎨",
    "MobileNumber": "📱",
    "RTOName": "🏢",
    "InsuranceUpto": "🛡️",
    "RCExpiryDate": "📄",
    "ChassisNumber": "🔩",
    "EngineNumber": "⚙️",
    "VehicleClass": "🚙",
    "Manufacturer": "🏭",
    "Financer": "💸",
    "PUCCExpiry": "📆"
}


def format_dict(data: dict) -> str:
    lines = []
    for k, v in data.items():
        if not v:
            continue
        emoji = EMOJIS.get(k, "•")
        label = k.replace("_", " ").title()
        val = str(v).replace("!", ", ").replace(",,", ",").strip(" ,")
        lines.append(f"{emoji} <b>{label}</b>: {val}")
    return "\n".join(lines)


def format_list(data_list: list) -> str:
    result = []
    for idx, item in enumerate(data_list, start=1):
        block = f"<b>📄 Result {idx}⃣</b>\n{format_dict(item)}"
        result.append(block)
    return "\n\n".join(result)


async def searching_message(ctx: ContextTypes.DEFAULT_TYPE, user: Update, what="info"):
    return await ctx.bot.send_message(
        chat_id=user.effective_chat.id,
        text=f"🔍 <b>Searching {what} for you</b> {user.effective_user.mention_html()}...",
        parse_mode=ParseMode.HTML,
    )


async def delete_after_60_seconds(ctx, message):
    await asyncio.sleep(60)
    try:
        await ctx.bot.delete_message(
            chat_id=message.chat_id,
            message_id=message.message_id
        )
    except:
        pass


async def phone_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "📱 Please enter a phone number.\nExample: /phone 8298339610"
        )
        return

    num = context.args[0]
    searching = await searching_message(context, update, "phone info")

    try:
        response = requests.get(
            f"https://measure-placement-maximize-pension.trycloudflare.com/search?mobile={num}"
        )
        json_data = response.json()
        data_list = json_data if isinstance(json_data, list) else json_data.get("data", [])

        if not data_list:
            await searching.edit_text(
                f"❌ No data found for <b>{num}</b>",
                parse_mode=ParseMode.HTML
            )
            return

        result = (
            f"{update.effective_user.mention_html()}\n\n"
            f"<b>📞 Phone Number Info:</b>\n{format_list(data_list)}\n\n"
            f"⚠️ Auto deleted in 1 min.\n🛠️ <i>By RDX_Hacker | <a href='{CHANNEL_USERNAME}'>Our Channel</a></i>"
        )
        await searching.edit_text(
            result,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        asyncio.create_task(delete_after_60_seconds(context, searching))

    except Exception as e:
        await searching.edit_text(
            f"❌ Error while fetching phone info.\n<code>{e}</code>",
            parse_mode=ParseMode.HTML
        )


async def aadhar_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "🆔 Please enter an Aadhaar number.\nExample: /aadhar 123456789012"
        )
        return

    aid = context.args[0]
    searching = await searching_message(context, update, "aadhar info")

    try:
        response = requests.get(
            f"https://measure-placement-maximize-pension.trycloudflare.com/search?aadhar={aid}"
        )
        json_data = response.json()
        data_list = json_data if isinstance(json_data, list) else json_data.get("data", [])

        if not data_list:
            await searching.edit_text(
                f"❌ No data found for <b>{aid}</b>",
                parse_mode=ParseMode.HTML
            )
            return

        result = (
            f"{update.effective_user.mention_html()}\n\n"
            f"<b>🆔 Aadhaar Info:</b>\n{format_list(data_list)}\n\n"
            f"⚠️ Auto deleted in 1 min.\n🛠️ <i>By RDX_Hacker | <a href='{CHANNEL_USERNAME}'>Our Channel</a></i>"
        )
        await searching.edit_text(
            result,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        asyncio.create_task(delete_after_60_seconds(context, searching))

    except Exception as e:
        await searching.edit_text(
            f"❌ Error while fetching Aadhaar info.\n<code>{e}</code>",
            parse_mode=ParseMode.HTML
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🚀 Welcome to <b>RDX_Hacker</b> OSINT Bot!\n"
        f"Join our updates: <a href='{CHANNEL_USERNAME}'>Crazy Earning</a>\n"
        f"Use /phone or /aadhar",
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )


# ========== RUN BOT ==========

def run_bot():
    app = Application.builder().token(BOT_TOKEN).concurrent_updates(True).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("phone", phone_lookup))
    app.add_handler(CommandHandler("aadhar", aadhar_lookup))
    print("🚀 Bot is running as RDX_Hacker...")
    app.run_polling()


if __name__ == "__main__":
    run_bot()