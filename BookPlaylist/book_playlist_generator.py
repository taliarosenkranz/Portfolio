import os
from langchain_openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")

# paste own api key for testing
#OPEN_AI_KEY = ""

llm = OpenAI(openai_api_key=os.environ["OPEN_AI_KEY"], temperature=0.6)


def keywords(chapter, book, author):
    keyword_prompt = f'what key words would you use to best describe the mood and happenings of chapter {chapter} of the book {book} by {author}?'
    key_words = llm.predict(keyword_prompt)
    return key_words


def music_recomender(keywords, chapter, book, author, num_songs):
    music_prompt = f'based on the keywords {keywords} to describe the book {book} by {author}, recommend {num_songs} songs that best reflect the mood of the keywords thus the book? The music must be instrumental.'
    music_reco = llm.predict(music_prompt)
    return music_reco

#print(f'keywords: {key_words}')
#print(f'music: {music_reco}')


print("YAY THIS WORKED!")
