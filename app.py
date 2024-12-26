from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Load data
movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Ensure the columns exist in the DataFrame
required_columns = ['movie_id', 'original_title', 'overview', 'genres', 'keywords', 'cast', 'crew']
for col in required_columns:
    if col not in movies.columns:
        print(f"Error: Column {col} is missing in the dataset")

similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    movie_index = movies[movies['original_title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]  # Top 10

    recommended_movies = []
    for i in movie_list:
        recommended_movies.append({
            'movie_id': movies.iloc[i[0]].get('movie_id', 'N/A'),
            'title': movies.iloc[i[0]].get('original_title', 'N/A'),
            'overview': movies.iloc[i[0]].get('overview', 'N/A'),
            'genres': movies.iloc[i[0]].get('genres', 'N/A'),
            
            'cast': movies.iloc[i[0]].get('cast', 'N/A'),
            'crew': movies.iloc[i[0]].get('crew', 'N/A')
        })
    return recommended_movies

@app.route('/', methods=['GET', 'POST'])
def index():
    movie_list = movies['original_title'].values
    recommendations = []
    selected_movie = None

    if request.method == 'POST':
        selected_movie = request.form.get('movie')
        if selected_movie in movie_list:
            recommendations = recommend(selected_movie)
        else:
            recommendations = [{'title': 'Movie not found'}]

    return render_template('index.html', movies=movie_list, recommendations=recommendations, selected_movie=selected_movie)

if __name__ == '__main__':
    app.run(debug=True)
