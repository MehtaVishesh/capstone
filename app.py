from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load embeddings and your data (replace with actual data paths)
embeddings = np.load('embeddings.npy')
df = pd.read_csv('3A2M.csv')
model = SentenceTransformer('distilbert-base-nli-mean-tokens')

@app.route('/', methods=['GET'])
def show_form():
    return render_template('index.html')

@app.route('/recc', methods=['POST'])
def recommend():
    data = request.get_json()
    ingredients = data['ingredients']

    # Your recommendation logic here
    recommendations = give_recommendations(ingredients)

    return jsonify({'recommendations': recommendations})

def give_recommendations(ingredients):
    cos_sim_data_2 = pd.DataFrame(cosine_similarity(embeddings, model.encode(ingredients)))
    cos_sim_data_2['Summed_Column'] = cos_sim_data_2.sum(axis=1)
    index_recomm = cos_sim_data_2["Summed_Column"].sort_values(ascending=False).index.tolist()[1:5]
    food_dish_recomm = df["title"].loc[index_recomm].values
    recipes_of_recomm = df["directions"].loc[index_recomm]
    ingredients_of_recomm = df["NER"].loc[index_recomm]

    recommendations = []
    for title, ingredients, recipe in zip(food_dish_recomm, ingredients_of_recomm, recipes_of_recomm):
        recommendation = {
            'title': title,
            'ingredients': ingredients,
            'recipe': recipe
        }
        recommendations.append(recommendation)

    return {'recommendations': recommendations}

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=500)
