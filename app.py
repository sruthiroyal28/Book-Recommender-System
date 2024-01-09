from flask import Flask , render_template , request
import pickle
import pandas as pd 
import numpy as np

popular_df = pd.read_pickle('data.pkl')
books = pd.read_pickle('books.pkl')
table = pd.read_pickle('table.pkl')
similarity_score = pd.read_pickle('similarity_matrix.pkl')
#popular_df = pickle.load(open('data.pkl','rb'))
#creating flask object
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                            book_name = list(popular_df['Book-Title'].values),
                            image = list(popular_df['Image-URL-M'].values),
                            author = list(popular_df['Book-Author'].values),
                            votes = list(popular_df['num_ratings'].values),
                            rating = list(popular_df['avg_rating'].values)
                            )   

@app.route('/recommend')
def recommend_fun():
    return render_template('recommend.html')

@app.route('/recommend_books_now',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(table.index==user_input)[0][0]
    #now we have to fetch the similarity scores assciated with the given book through it's index
    similar_items = sorted(list(enumerate(similarity_score[index])),key=lambda x : x[1],reverse=True)[1:6]
    
    data=[]
    for i in similar_items:
        item=[]
        #print(i[0])#prints the indexes that are similar to given book
        #print(table.index[i[0]])#prints the book title which is index in the 'table' based on the zero-indexing
        #print(books[books['Book-Title']  == table.index[i[0]]])#same books might have different isbn numbers so we drop the duplicates
        tmp_df = books[books['Book-Title']  == table.index[i[0]]]
        item.extend(list(tmp_df.drop_duplicates('Book-Title')['Book-Title'].values))#if we don't convert to list it will be of the form numpy array
        item.extend(list(tmp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(tmp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))#extends the original list 
        
        data.append(item)
    print(data)
    return render_template('recommend.html',data=data)


if __name__=='__main__':
    app.run(debug=True)