from flask import Flask, render_template , request
import pickle
import numpy as np



popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pivot_table.pkl' , 'rb'))
books = pickle.load(open('books.pkl' , 'rb'))
similarity_score = pickle.load(open('similarity_df.pkl' , 'rb'))
final = pickle.load(open('final.pkl' , 'rb'))
similarity_scores = pickle.load(open('similarity_score.pkl' , 'rb'))
pt_content = pickle.load(open('pt_content.pkl' , 'rb'))




app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html' ,
                           book_name =list(popular_df['Book-Title'].values),
                           author =list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_rating'].values),
                           ratings=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    global result
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    temp = list(similarity_score.sort_values([user_input], ascending=True).head(10).index)
    book_list = []
    data = []
    for i in temp:
        book_list = book_list + list(final[final['User_ID'] == i]['Book_Title'])
        result = set(book_list) - set(final[final['User_ID'] == user_input]['Book_Title'])
        result = list(result)[:10]
    for i in result:
        item = []
        temp_df = books[books['Book-Title'] == i]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html', data=data)



@app.route('/content')
def books_ui():
    return render_template('content.html')


@app.route('/content_books', methods=['post'])
def book_recommend():
    input = request.form.get('input')
    index = np.where(pt_content.index == input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:10]
    book = []
    for i in similar_items:
        items = []
        temp_df = books[books['Book-Title'] == pt_content.index[i[0]]]
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        book.append(items)


    print(book)

    return render_template('content.html', data=book)



if __name__ == '__main__':
    app.run(debug=True)