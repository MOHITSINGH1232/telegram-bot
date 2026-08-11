import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = "YOUR_NEW_BOT_TOKEN"
FEEDBACK = "MOHITSELLER0"

PANELS = {
    "drip": ("🛒 DRIP SILENT APK-MOD",
             [("1 DAY", 90), ("3 DAYS", 200), ("7 DAYS", 330), ("15 DAYS", 650), ("30 DAYS", 1350)]),

    "silent": ("🛒 SILENT CHEATS APK MOD",
               [("1 DAY", 90), ("3 DAYS", 200), ("7 DAYS", 330), ("15 DAYS", 650), ("30 DAYS", 1350)]),

    "prime": ("🛒 PRIME HOOK APK-MOD",
              [("1 DAY", 95), ("3 DAYS", 200), ("7 DAYS", 335), ("15 DAYS", 650), ("30 DAYS", 1350)]),

    "hg": ("🛒 HG CHEATS APK-MOD",
           [("1 DAY", 95), ("7 DAYS", 335), ("10 DAYS", 500), ("30 DAYS", 1350)]),

    "pato": ("🛒 PATO TEAM APK-MOD",
             [("3 DAYS", 260), ("7 DAYS", 360), ("15 DAYS", 700), ("30 DAYS", 1400)]),

    "bala": ("🛒 BALA MOD XYZ CHEATS",
             [("1 HOUR", 70), ("3 HOURS", 150), ("6 HOURS", 330), ("12 HOURS", 650), ("24 HOURS", 1250)]),

    "br": ("🛒 BR MOD ROOT",
           [("1 DAY", 95), ("3 DAYS", 230), ("7 DAYS", 490), ("15 DAYS", 930), ("30 DAYS", 1400)]),

    "haxx": ("🛒 HAXX-CKER PRO ROOT",
             [("10 DAYS", 590), ("20 DAYS", 1200), ("30 DAYS", 1800), ("600 DAYS", 2900)]),

    "silentroot": ("🛒 SILENT CHEATS ROOT",
                   [("1 DAY", 90), ("3 DAYS", 200), ("7 DAYS", 330), ("14 DAYS", 600), ("28 DAYS", 1200)]),

    "migul": ("🛒 MIGUL IPHONE IOS FF",
              [("1 DAY", 220), ("7 DAYS", 800), ("30 DAYS", 1450)]),

    "kos": ("🛒 KOS FF ROOT ANDROID",
            [("1 DAY", 100), ("7 DAYS", 500), ("30 DAYS", 1300)]),

    "rapid": ("🛒 RAPID CORE ROOT",
              [("1 DAY", 95), ("7 DAYS", 450), ("14 DAYS", 850), ("30 DAYS", 1300)]),
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("🛒 BUY NOW", callback_data="buy")],
        [InlineKeyboardButton("💬 FEEDBACK", url=f"https://t.me/{FEEDBACK}")],
    ]

    await update.message.reply_text(
 "🔥 MOHIT PANEL STORE 🔥\n\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    buttons = [
        [InlineKeyboardButton(name, callback_data=f"panel:{key}")]
        for key, (name, plans) in PANELS.items()
    ]

    buttons.append([
        InlineKeyboardButton("💬 FEEDBACK", url=f"https://t.me/{FEEDBACK}")
    ])

    await q.edit_message_text(
        "🛒 CHOOSE YOUR PANEL:",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    key = q.data.split(":")[1]
    name, plans = PANELS[key]

    text = f"{name}\n\n💰 CHOOSE YOUR ACCESS PLAN:\n\n"
    buttons = []

    for i, (duration, price) in enumerate(plans):
        text += f"💵 ₹{price} — 🛒 {duration}\n"

        buttons.append([
            InlineKeyboardButton(
                f"🛒 {duration} — ₹{price}",
                callback_data=f"plan:{key}:{i}",
            )
        ])

    buttons.append([
        InlineKeyboardButton("⬅️ BACK", callback_data="buy")
    ])

    await q.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    _, key, index = q.data.split(":")
    name, plans = PANELS[key]
    duration, price = plans[int(index)]

    buttons = [
        [
            InlineKeyboardButton(
                "💰 PAY UPI",
                callback_data=f"upi:{key}:{index}",
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ BACK",
                callback_data=f"panel:{key}",
            )
        ],
        [
            InlineKeyboardButton(
                "💬 FEEDBACK",
                url=f"https://t.me/{FEEDBACK}",
            )
        ],
    ]

    await q.edit_message_text(
        f"🛒 ORDER SUMMARY\n\n"
        f"📄 {name}\n"
        f"⏱️ {duration}\n"
        f"💰 ₹{price}\n\n"
        f"Tap PAY UPI to continue.",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def expire_order(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    qr_message_id: int,
    key: str,
    index: int,
):
    await asyncio.sleep(300)  # 5 minutes

    # Delete QR/payment message
    try:
        await context.bot.delete_message(
            chat_id=chat_id,
            message_id=qr_message_id,
        )
    except Exception:
        pass

    # Send expiry message
    name, plans = PANELS[key]
    duration, price = plans[int(index)]

    buttons = [
        [
            InlineKeyboardButton(
                "🛒 TRY AGAIN",
                callback_data=f"retry:{key}:{index}",
            )
        ]
    ]

    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "❌ PAYMENT FAILED\n\n"
            f"Your QR for 💵 ₹{price} expired because "
            "no payment was received within 5 minutes.\n\n"
            f"📦 {name}\n"
            f"⏱️ {duration}\n"
            f"💰 ₹{price}\n\n"
            "You can try buying again anytime."
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
    )

    context.user_data.pop("payment_task", None)


async def upi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    _, key, index = q.data.split(":")
    name, plans = PANELS[key]
    duration, price = plans[int(index)]

    # Cancel previous timer if user starts another order
    old_task = context.user_data.get("payment_task")

    if old_task:
        old_task.cancel()

    # Send QR
    with open("qr.jpg", "rb") as qr_file:
        qr_message = await q.message.reply_photo(
            photo=qr_file,
            caption=(
                "💰 PAYMENT\n\n"
                f"📦 {name}\n"
                f"⏱️ {duration}\n"
                f"💵 ₹{price}\n\n"
                f"📲 Scan this QR and pay ₹{price}.\n\n"
                "⏳ QR Session TTL: expires in 5 minutes."
            ),
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "✅ VERIFY PAYMENT",
                        callback_data=f"verify:{key}:{index}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "👉 CANCEL ORDER",
                        callback_data=f"cancel:{key}:{index}",
                    )
                ],
            ]),
        )

    # Start 5-minute timer
    task = asyncio.create_task(
        expire_order(
            context,
            q.message.chat_id,
            qr_message.message_id,
            key,
            int(index),
        )
    )

    context.user_data["payment_task"] = task


async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer("Order cancelled.")

    # Stop timer
    task = context.user_data.pop("payment_task", None)

    if task:
        task.cancel()

    # Remove QR message
    try:
        await q.message.delete()
    except Exception:
        pass

    await context.bot.send_message(
        chat_id=q.message.chat_id,
        text="❌ Order cancelled.\n\nQR payment session removed.",
    )


async def verify_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    await q.message.reply_text(
        "⏳ Payment verification requested.\n\n"
        "Please wait while the payment is checked."
    )


async def retry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    _, key, index = q.data.split(":")
    name, plans = PANELS[key]
    duration, price = plans[int(index)]

    buttons = [
        [InlineKeyboardButton("⬅️ BACK", callback_data=f"panel:{key}")],
        [InlineKeyboardButton("💬 FEEDBACK", url=f"https://t.me/{FEEDBACK}")]
    ]

    buttons.append([
    InlineKeyboardButton(
        "💰 PAY UPI",
        callback_data=f"upi:{key}:{index}"
    )
])

    await q.edit_message_text(
    f"🛒 ORDER SUMMARY\n\n"
    f"📄 {name}\n"
    f"⏱️ {duration}\n"
    f"💰 ₹{price}\n\n",
        reply_markup=InlineKeyboardMarkup(buttons),
    )
async def upi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    _, key, index = q.data.split(":")
    name, plans = PANELS[key]
    duration, price = plans[int(index)]

    await q.message.reply_photo(
        photo=open("qr.jpg", "rb"),
        caption=(
            f"💰 PAYMENT\n\n"
            f"📦 {name}\n"
            f"⏱ {duration}\n"
            f"💵 ₹{price}\n\n"
            f"📲 Scan this QR and pay ₹{price}."
        )
    )
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(panel, pattern="^panel:"))
    app.add_handler(CallbackQueryHandler(plan, pattern="^plan:"))
    app.add_handler(CallbackQueryHandler(buy, pattern="^buy$"))
    app.add_handler(CallbackQueryHandler(upi, pattern="^upi:"))
    app.run_polling()
if __name__ == "__main__":
    main(    )
