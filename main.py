from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Данные о товарах
PRODUCTS = {
    "Рыба": {
        "Стейки": [
            {"name": "Осетра", "price": 4900, "unit": "1 кг"},
            {"name": "Белуги", "price": 7000, "unit": "1 кг"},
            {"name": "Чавычи", "price": 3900, "unit": "1 кг (Камчатка)"},
            {"name": "Сёмги", "price": 3100, "unit": "1 кг (Мурманск)"},
            {"name": "Кижуча", "price": 2800, "unit": "1 кг (Камчатка)"},
        ],
        "Копчёная рыба": [
            {"name": "Сёмга подкопчённая", "price": 5200, "unit": "1 кг"},
            {"name": "Чавыча х/к", "price": 6000, "unit": "1 кг (Камчатка)"},
            {"name": "Палтус х/к", "price": 3100, "unit": "1 кг (Камчатка)"},
        ],
        "Вяленая рыба": [
            {"name": "Корюшка", "price": 3000, "unit": "1 кг (Камчатка)"},
            {"name": "Камбала-Ёрш", "price": 1600, "unit": "1 кг (Мурманск)"},
        ],
    },
    "Икра": [
        {"name": "Нерки", "price": 5200, "unit": "0.5 кг (Камчатка)"},
        {"name": "Кижуча", "price": 5500, "unit": "0.5 кг"},
        {"name": "Горбуши", "price": 4900, "unit": "0.5 кг"},
        {"name": "Кеты", "price": 5500, "unit": "0.5 кг"},
    ],
    "Крабы": [
        {"name": "Фаланга гигант", "price": 8500, "unit": "1 кг"},
        {"name": "Кулак краба", "price": 5000, "unit": "1 кг (Камчатка)"},
        {"name": "Салатное мясо краба", "price": 4500, "unit": "1 кг"},
    ],
}

# Стартовое сообщение
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton(category, callback_data=category)] for category in PRODUCTS
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Добро пожаловать в магазин Зов Океан! Выберите категорию:", reply_markup=reply_markup)

# Вывод категорий
def category_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    category = query.data

    if isinstance(PRODUCTS[category], dict):  # Подкатегории
        keyboard = [
            [InlineKeyboardButton(subcategory, callback_data=f"{category}:{subcategory}")]
            for subcategory in PRODUCTS[category]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text=f"Категория: {category}\nВыберите подкатегорию:", reply_markup=reply_markup)
    else:  # Товары
        items = PRODUCTS[category]
        text = "\n".join(
            [f"{item['name']} - {item['price']} руб ({item['unit']})" for item in items]
        )
        query.edit_message_text(text=f"Категория: {category}\n\n{text}")

# Вывод товаров из подкатегорий
def subcategory_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    category, subcategory = query.data.split(":")

    items = PRODUCTS[category][subcategory]
    text = "\n".join(
        [f"{item['name']} - {item['price']} руб ({item['unit']})" for item in items]
    )
    query.edit_message_text(text=f"Категория: {category} -> {subcategory}\n\n{text}")

# Основной обработчик
def main() -> None:
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(category_callback, pattern="^[^:]+$"))
    updater.dispatcher.add_handler(CallbackQueryHandler(subcategory_callback, pattern=".+:.+"))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
