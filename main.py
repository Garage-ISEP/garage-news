import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from dotenv import load_dotenv

from draw_instagram_news import draw_instagram_news
from from_news_to_summary import from_news_to_summary
from generate_stable_diffusion_image import generate_stable_diffusion_image
from get_latest_tech_news import get_latest_tech_news

load_dotenv()



TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")



LAB_MAPPING = {
    "🤖 IA": "IA",
    "⛓️ Blockchain": "Blockchain",
    "💻 Coder": "Coder",
    "🕶️ Meta": "Meta",
    "🛠️ Maker": "Maker",
    "🔒 Cyber": "Cyber",
    "🌍 All": "All"
}


def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(lab, callback_data=LAB_MAPPING[lab]) for lab in list(LAB_MAPPING.keys())[0:2]],
        [InlineKeyboardButton(lab, callback_data=LAB_MAPPING[lab]) for lab in list(LAB_MAPPING.keys())[2:4]],
        [InlineKeyboardButton(lab, callback_data=LAB_MAPPING[lab]) for lab in list(LAB_MAPPING.keys())[4:6]],
        [InlineKeyboardButton(lab, callback_data=LAB_MAPPING[lab]) for lab in list(LAB_MAPPING.keys())[6:]]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('For which lab do you want to create a post :', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    print(query.data)

    lab = query.data

    if lab == "All":
        for lab_key in list(LAB_MAPPING.keys())[:-1]:  # Process all labs except "All"
            create_news_summary_image(update, context, lab_key)
    else:
        create_news_summary_image(update, context, lab)

def create_news_summary_image(update: Update, context: CallbackContext, lab: str):
    # Get the latest news about the selected lab
    context.bot.send_message(chat_id=update.effective_chat.id, text='Processing... (Please do not spam)')

    if lab == "All":
        # Loop through all labs if "All" is selected
        for lab in LAB_MAPPING.values():
            news = get_latest_tech_news(lab)  # Assuming get_latest_tech_news() function takes lab as parameter
            summary, image_prompt = from_news_to_summary(news)
            generate_stable_diffusion_image(image_prompt, lab)
            final_image_path = draw_instagram_news(summary, "news_image.png", lab)
            chat_id = update.effective_chat.id
            context.bot.send_photo(chat_id=chat_id, photo=open(final_image_path, 'rb'))
    else:
        # Get news for the specific lab
        news = get_latest_tech_news(lab)  # Assuming get_latest_tech_news() function takes lab as parameter
        ##
        #news= """
        #Le cours se trouve au-delà de la trendline baissière initiée en novembre 2021, mais le cours ne parvient pour le moment pas à reprendre une dynamique avec des creux et des sommets ascendants. De plus, le cours est en train de glisser dangereusement sous la trendline haussière. Si le cours ne réagit pas rapidement, la trendline haussière et le biais institutionnel (EMA 9/EMA 18) baissier pourraient agir en tant que résistance. Dans ce cas, un retour au niveau du support à 480 milliards de dollars est possible. Toutefois, si les acheteurs se montrent rapidement, et que le cours casse la résistance hebdomadaire, le cours pourrait se développer en direction de la résistance à 950 milliards de dollars.

#Le RSI pourrait rebondit au niveau de la trendline haussière. Un rebond ici permettrait de conserver la dynamique initiée en juin 2022. Les acheteurs doivent rapidement réagir pour éviter de connaître une nouvelle vague de baisse.
 #       """

        summary, image_prompt = from_news_to_summary(news)
        generate_stable_diffusion_image(image_prompt, lab)
        final_image_path = draw_instagram_news(summary, "news_image.png", lab)
        chat_id = update.effective_chat.id
        context.bot.send_photo(chat_id=chat_id, photo=open(final_image_path, 'rb'))


def main():
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()