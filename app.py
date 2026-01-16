import streamlit as st
import pickle

st.set_page_config(page_title="🎬 Movie Recommender")

st.title("🎥 Movie Recommendation System")

# load files
movies = pickle.load(open("movies.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))
vectors = pickle.load(open("vectors.pkl", "rb"))

# lowercase lookup column (safety)
if "title_lower" not in movies.columns:
    movies["title_lower"] = movies["title"].fillna("").str.lower()

movie_input = st.text_input("Type a movie name")

def recommend(movie):
    movie = movie.lower()

    if movie not in list(movies["title_lower"]):
        return None

    idx = movies[movies["title_lower"] == movie].index[0]

    distances, indices = model.kneighbors(vectors[idx], n_neighbors=6)

    recs = [movies.iloc[i].title for i in indices[0][1:]]
    return recs


if st.button("Recommend"):
    if movie_input.strip() == "":
        st.warning("Please enter a movie name.")
    else:
        results = recommend(movie_input)

        if results is None:
            st.error("Movie not found.")
        else:
            st.subheader("Recommended Movies:")
            for r in results:
                st.write("👉", r)
