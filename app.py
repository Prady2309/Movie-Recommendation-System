import pandas as pd
import numpy as np
import pickle
import streamlit as st
import time
import requests
import itertools

st.set_page_config(
    page_title="Movie Recommender",
    page_icon=":clapper:"
)

url_link = "http://www.omdbapi.com/?apikey=7fb9704&t={}"

movie_dict = pickle.load(open('movies_df.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_title):
    url = url_link.format(movie_title)
    response = requests.get(url)
    data = response.json()
    path = data['Poster']
    # full_path = url_link + path
    return path

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]  
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommend_posters_link = []
    for i in movie_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        # Fetch poster from API
        # movie_title = movies.iloc[i[0]].title
        recommend_posters_link.append(fetch_poster(movie_title))
    
    # Loading animation
    placeholder = st.empty()
    placeholder.progress(25, "Loading......")
    time.sleep(0.5)
    placeholder.progress(65, "Loading......")
    time.sleep(0.5)
    placeholder.progress(100, "Loading......")
    time.sleep(0.5)
    placeholder.empty()

    return recommended_movies, recommend_posters_link

def search_movie(movie_title):
    url = url_link.format(movie_title)
    response = requests.get(url)
    movie_data = response.json()
    display_details(movie_data)

def get_duration(minutes):
    minutes = int(minutes.replace(' min', ''))

    # Get hours with floor division
    hours = minutes // 60

    # Get additional minutes with modulus
    minutes = minutes % 60

    # Create time as a string
    time_string = "{}hr {}min".format(hours, minutes)

    return time_string 

def get_rating(ratings):
    val = float(ratings) * 9.5 / 20
    return val

def display_details(movie_data):
    c1, c2 = st.columns(2)
    with c1:
        st.image(movie_data['Poster'])
    with c2:
        st.write("**Title:** {}".format(movie_data["Title"]))
        stars = '⭐' * int(round(get_rating(movie_data["imdbRating"])))
        st.write("**Ratings:** {}".format(stars))
        st.write("**Year:** {}".format(movie_data["Released"]))
        st.write("**Duration:** {}".format(get_duration(movie_data["Runtime"])))
        st.write("**Genres:** {}".format(movie_data["Genre"]))
        st.write("**Country:** {}".format(movie_data["Country"]))
        st.write("**Cast:** {}".format(movie_data["Actors"]))
        st.write("**Director:** {}".format(movie_data["Director"]))
        st.write("**Synopsis:** {}".format(movie_data["Plot"]))
        

# Streamlit
st.title("Movie Database")

options = ["Recommendation", "Search"]
selection = st.pills("Mode", options, selection_mode="single")

if selection == "Recommendation":

# tab1, tab2 = st.tabs(["Recommendations", "Search"])
# with tab1:
    select_movie_name = st.selectbox(
        'Select a movie',
        movies['title'].values)
    
    if st.button("Recommend", type="primary"):
        recommendations, movie_posters = recommend(select_movie_name)

    # for name in recommendations:
    #     st.write(name)

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
        # st.text(recommendations[0])
            st.image(movie_posters[0], caption=recommendations[0])
        with col2:
        # st.text(recommendations[1])
            st.image(movie_posters[1], caption=recommendations[1])

        with col3:
        # st.text(recommendations[2])
            st.image(movie_posters[2], caption=recommendations[2])
        with col4:
        # st.text(recommendations[3])
            st.image(movie_posters[3], caption=recommendations[3])
        with col5:
        # st.text(recommendations[4])
            st.image(movie_posters[4], caption=recommendations[4])

# with tab2:
elif selection == "Search":
    search_title = st.selectbox(
        'Search the movie title',
        movies['title'].values)
    
    if st.button("Search", type="primary"):
        search_movie(search_title)
    



