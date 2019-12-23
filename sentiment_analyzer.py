from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
import re
import pickle

class SentimentAnalyzer:
    final_model_path = 'data/model_cache/final_model.sav'
    vocabulary_path = 'data/model_cache/vocabulary.pkl'
    data_train_path = 'data/movie_data/full_train.txt'
    data_test_path = 'data/movie_data/full_test.txt'

    def preprocess_reviews(self, reviews):
        REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
        REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
        reviews = [REPLACE_NO_SPACE.sub("", line.lower()) for line in reviews]
        reviews = [REPLACE_WITH_SPACE.sub(" ", line) for line in reviews]

        return reviews
    
    def load_model(self, train_required):       
        if train_required:
            self.train()
        else: 
            self.load()
    
    def load(self):
        self.final_model = pickle.load(open(SentimentAnalyzer.final_model_path, 'rb'))
        self.cv = CountVectorizer(binary=True, vocabulary=pickle.load(open(SentimentAnalyzer.vocabulary_path, "rb")))

    def train(self):        
        print("Training...")

        # data preprocessing
        reviews_train = []
        for line in open(SentimentAnalyzer.data_train_path, encoding='utf8', mode='r'):
            reviews_train.append(line.strip())

        reviews_test = []
        for line in open(SentimentAnalyzer.data_test_path, encoding='utf8', mode='r'):
            reviews_test.append(line.strip())

        reviews_train_clean = self.preprocess_reviews(reviews_train)
        reviews_test_clean = self.preprocess_reviews(reviews_test)

        # vectorization  
        self.cv = CountVectorizer(binary=True)        
        self.cv.fit(reviews_train_clean)
        X = self.cv.transform(reviews_train_clean)
        X_test = self.cv.transform(reviews_test_clean)        

        # the first 12.5k reviews are positive and the last 12.5k are negative.
        target = [1 if i < 12500 else 0 for i in range(25000)]

        X_train, X_val, y_train, y_val = train_test_split(X, target, train_size=0.75)

        # choosing the best hyperparameter C which adjust regularization
        accuracy = 0
        c = 0
        for current_c in [0.01, 0.05, 0.25, 0.5, 1]:
            lr = LogisticRegression(C=current_c, solver='liblinear')
            lr.fit(X_train, y_train)
            current_accuracy = accuracy_score(y_val, lr.predict(X_val))
            if current_accuracy > accuracy:
                accuracy = current_accuracy
                c = current_c
            print(f"Accuracy for C = {current_c}: {current_accuracy}")

        print(f"The best accuracy is {accuracy}, C = {c}")

        # train final model
        self.final_model = LogisticRegression(C=c,  solver='liblinear')
        self.final_model.fit(X, target)
        print(f"Final accuracy is {accuracy_score(target, self.final_model.predict(X_test))}")

        # save final model       
        pickle.dump(self.final_model, open(SentimentAnalyzer.final_model_path, 'wb'))
        pickle.dump(self.cv.vocabulary_, open(SentimentAnalyzer.vocabulary_path,"wb"))

    def predict(self, new_review):
        # predict on new review        
        new_review_clean = self.preprocess_reviews([new_review])
        X_new_review = self.cv.transform(new_review_clean)
        y_new_review = self.final_model.predict(X_new_review)
        return y_new_review
