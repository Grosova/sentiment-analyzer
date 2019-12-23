from sentiment_analyzer import SentimentAnalyzer
import json
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
app.config.from_pyfile('config.py')

movies_list = []
sa = SentimentAnalyzer()

@app.route('/')
def movies():
    with open('data/movies_list.json') as f:
        data = json.load(f)
        movies_list=data["movies"]
    return render_template('index.html', movies=movies_list)

@app.route('/send/<movie_id>', methods=['POST'])
def send(movie_id):    
    feedback = request.form['feedback']
    res = sa.predict(feedback)
    
    return json.dumps({'status':'OK', 'res':str(res[0])})

if __name__ == '__main__':
    train_model = app.config['TRAIN']    
    sa.load_model(train_model)
    app.run()    