from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

#popular_df = pickle.load(open('popular_book.pkl', 'rb'))
popular_df = pd.read_pickle('popular_book.pkl')
pt = pickle.load(open('pivot_table.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_score.pkl', 'rb'))

application = Flask(__name__,template_folder='template')

@application.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_rating'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@application.route('/recommendation')
def recommend_ui():
    return render_template('recommendation.html')

@application.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommendation.html',data=data)

if __name__ == '__main__':
    application.run(debug=True)