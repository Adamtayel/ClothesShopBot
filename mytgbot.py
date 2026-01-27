import csv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8449330341:AAFyYfJzWEEOs2rGnLq8zXB6TrLnbSLpDj4"

# read type
products_by_type = {}
with open("products.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        product_type = row["Type"]
        if product_type not in products_by_type:
            products_by_type[product_type] = []
        products_by_type[product_type].append(row)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Tayel.clo store , Our work hours from 10 pm to 10 am , to see our products click /products 😊 ")

#show products type 
async def show_types(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(ptype, callback_data=f"type|{ptype}")] for ptype in products_by_type]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("choose the type 🤔 :", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    if data.startswith("type|"):
        product_type = data.split("|")[1]
        products = products_by_type[product_type]
        
        for p in products:
            # تنظيف URL
            image_url = p['ImageUrl'].strip()
            
            message = (
                f"Name: {p['Name']}\n"
                f"Sizes: {p['Sizes']}\n"
                f"Price: {p['Price']}\n"
                f"Material: {p['Material']}\n"
                f"Gender: {p['Gender']}"
            )
            
        # send img + msg
            try:
                await query.message.reply_photo(photo=image_url, caption=message)
            except:
              
                await query.message.reply_text(f"{message}\n(photo not ready now)")



def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("products", show_types))
    app.add_handler(CallbackQueryHandler(button))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
