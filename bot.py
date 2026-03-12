from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 1. Replace with your actual Token from @BotFather
TOKEN = "YOUR_ACTUAL_BOT_TOKEN"
# 2. Replace with your actual bot username (without the @)
BOT_USERNAME = "YOUR_BOT_USERNAME"

# Dictionary to store referrals: {user_id: count}
users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    first_name = update.effective_user.first_name

    # Handle Referral Logic
    if context.args:
        referrer_id = context.args[0]
        
        # Ensure user isn't referring themselves and check if this is a new start
        if referrer_id != user_id:
            # Simple logic: increment referrer's count
            # Note: In production, check if user_id is already in your DB to prevent spam
            users[referrer_id] = users.get(referrer_id, 0) + 1

    # Generate the unique referral link for the current user
    referral_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
    
    # Get current user's total invites
    total_invites = users.get(user_id, 0)

    text = (
        f"Welcome {first_name}!\n\n"
        f"Your referral link:\n{referral_link}\n\n"
        f"Total invites: {total_invites}"
    )

    await update.message.reply_text(text)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    
    print("Bot is running...")
    app.run_polling()
