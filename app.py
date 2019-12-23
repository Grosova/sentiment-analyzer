from sentiment_analyzer import SentimentAnalyzer
import json
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

movies_list = []

@app.route('/')
def movies():
    with open('data/movies_list.json') as f:
        data = json.load(f)
        movies_list=data["movies"]
    return render_template('index.html', movies=movies_list)

@app.route('/send/<movie_id>', methods=['POST'])
def send(movie_id):    
    feedback = request.form['feedback'] 
       
    sa = SentimentAnalyzer()
    sa.create_model(False)
    res = sa.predict(feedback)   
    
    return json.dumps({'status':'OK', 'res':str(res[0])})

if __name__ == '__main__':
    app.run(debug=True)