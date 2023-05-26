import openai
import os
from dotenv import load_dotenv

load_dotenv()



openai.api_key = os.getenv("OPENAI_APIKEY")

def from_news_to_summary(text):
    prompt = f"Create a short article of 4 sentences, easy-to-understand tech news summary in french for teenagers based on the following article, do not exceed 400 characters:\n\n{text}"

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


