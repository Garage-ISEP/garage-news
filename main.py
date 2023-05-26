import textwrap
import os
import time
import requests
from newscatcherapi import NewsCatcherApiClient
import openai
from PIL import Image, ImageDraw, ImageFont
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv
import json

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
openai.api_key = os.getenv("OPENAI_APIKEY")
NEWS_CATCHER_API = os.getenv("NEWS_CATCHER")
STABLE_DIFFUSION_API_KEY = os.getenv("STABLE_DIFFUSION_API_KEY")


def get_latest_tech_news():
    themes = ["blockchain", "artificial intelligence", "programming and coding",
              "virtual reality", "cyber security", "electronics and robotics"]

    news_articles = []

    # Get your API key from https://newscatcherapi.com/
    newscatcher = NewsCatcherApiClient(x_api_key=NEWS_CATCHER_API)

    for theme in themes:
        # Query the latest news about the theme
        result = newscatcher.get_search(q=theme, lang="en", page_size=1)
        # Choose the latest news
        latest_news = result['articles'][0]
        print(latest_news)
        news_articles.append(latest_news)
        time.sleep(1.5)

    return news_articles

def get_latest_tech_news_test():
    theme = "virtual reality, metaverse, augmented reality"

    # Get your API key from https://newscatcherapi.com/
    newscatcher = NewsCatcherApiClient(x_api_key=NEWS_CATCHER_API)

    # Query the latest news about the theme
    result = newscatcher.get_search(q=theme, lang="en", page_size=1)

    # Choose the latest news
    latest_news = result['articles'][0]

    return latest_news


def generate_tech_news_summary(text):
    prompt = f"Create a short article of 4 sentences, easy-to-understand tech news summary in french for teenagers based on the following article:\n\n{text}"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=400,
        n=1,
        stop=None,
        temperature=0.5,
    )

    summary = response.choices[0].text.strip()
    print(summary)

    image_prompt = f"Create an image based on the following tech news summary for teenagers:\n\n{summary}"

    return summary, image_prompt


import json

import json

def generate_stable_diffusion_image(prompt):
    url = "https://stablediffusionapi.com/api/v3/text2img"
    payload = json.dumps({
      "key": STABLE_DIFFUSION_API_KEY,  # you should set this to your actual Stable Diffusion API key
      "prompt": prompt,
      "negative_prompt": None,
      "width": "1080",
      "height": "1080",
      "samples": "1",
      "num_inference_steps": "20",
      "seed": None,
      "guidance_scale": 7.5,
      "safety_checker": "yes",
      "multi_lingual": "no",
      "panorama": "no",
      "self_attention": "no",
      "upscale": "no",
      "embeddings_model": "embeddings_model_id",
      "webhook": None,
      "track_id": None
    })

    headers = {
      'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        image_url = response.json()['output'][0]
        image = Image.open(requests.get(image_url, stream=True).raw)
        image.save("news_image.png")
    except Exception as e:
        print("Error generating image:", e)


def justify(line, font, width):
    words = line.split()
    spaces_to_fill = width - sum(font.getsize(word)[0] for word in words)
    if len(words) == 1:
        return line
    spaces_to_add = spaces_to_fill // (len(words) - 1)
    justified_line = ''
    for word in words[:-1]:
        justified_line += word + '  ' * (font.getsize(' ')[0] + spaces_to_add)
    justified_line += words[-1]
    return justified_line


def generate_newspost(text_description, generated_image_path, lab):
    background_image = Image.new('RGB', (1080, 1080), color=(255, 255, 255))
    generated_image = Image.open("news_image.png")
    lab_image = Image.open(f'assets/{lab}_news.png')

    background_image.paste(generated_image, (0, 0))
    background_image.paste(lab_image, (0, 0), lab_image)

    d = ImageDraw.Draw(background_image)
    font = ImageFont.truetype('fonts/OpenSans-Regular.ttf', 40)

    # Prepare the text for automatic line wrapping
    wrapped_text = textwrap.wrap(str(text_description), width=50)  # Maximum line width

    # Display each line of text with a different y-coordinate
    y_position = 420
    for line in wrapped_text:
        d.text((45, y_position), line, font=font, fill=(255, 255, 255))
        y_position += 50  # Add vertical space between lines

    background_image.save('final_image.png')
    return 'final_image.png'


def create_news_summary_image(update: Update, context: CallbackContext):
    # Get the latest news about blockchain
    #news = get_latest_tech_news()
    news = get_latest_tech_news_test()
    print(news)
    # Create a summary with GPT API
    summary, image_prompt = generate_tech_news_summary(news)

    # Generate an image with stable diffusion
    generate_stable_diffusion_image(image_prompt)

    # Generate newspost image
    final_image_path = generate_newspost(summary, "news_image.png", "vr")

    # Send the image to the chat
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(final_image_path, 'rb'))

    print("News summary image generated and sent")


def main():
    # Instantiate the updater and dispatcher
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Add handlers for the /start and /name commands
    dispatcher.add_handler(CommandHandler("start", create_news_summary_image))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
