import streamlit as st
from book_playlist_generator import keywords
from book_playlist_generator import music_recomender


st.title("Book Playlist Generator")
st.write(
    "Fully dive into the world of your book with music recommended according to each chapter")

book_name = st.text_input("Book Name")
author_name = st.text_input("Author Name")
num_chapter = st.text_input(f'What Chapter of {book_name}?')
num_songs = st.selectbox(f'Select the number of songs you would like to have recommended for chapter {num_chapter}', [
    "1", "2", "3", "5", "10"])

if st.button("Generate Playlist"):
    key_words = keywords(num_chapter, book_name, author_name)
    music_recomended = music_recomender(
        key_words, num_chapter, book_name, author_name, num_songs)
    st.write(
        f'Enjoy this music while reading chapter {num_chapter}, of {book_name} by {author_name}: ')
    st.write(music_recomended)


