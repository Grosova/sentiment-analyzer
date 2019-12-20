# data preprocessing
import re

REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")

def preprocess_reviews(reviews):
    reviews = [REPLACE_NO_SPACE.sub("", line.lower()) for line in reviews]
    reviews = [REPLACE_WITH_SPACE.sub(" ", line) for line in reviews]

    return reviews

reviews_train = []
for line in open('movie_data/full_train.txt', encoding='utf8', mode='r'):
    reviews_train.append(line.strip())

reviews_test = []
for line in open('movie_data/full_test.txt', encoding='utf8', mode='r'):
    reviews_test.append(line.strip())

reviews_train_clean = preprocess_reviews(reviews_train)
reviews_test_clean = preprocess_reviews(reviews_test)

# vectorization
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(binary=True)
cv.fit(reviews_train_clean)
X = cv.transform(reviews_train_clean)
X_test = cv.transform(reviews_test_clean)

# building classifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# the first 12.5k reviews are positive and the last 12.5k are negative.
target = [1 if i< 12500 else 0 for i in range(25000)]

X_train, X_val, y_train, y_val = train_test_split(X, target, train_size = 0.75)

# choosing the best hyperparameter C which adjust regularization
accuracy = 0
c = 0
for current_c in [0.01, 0.05, 0.25, 0.5, 1]:
    lr = LogisticRegression(C = current_c)
    lr.fit(X_train, y_train)    
    current_accuracy =  accuracy_score(y_val, lr.predict(X_val))
    if current_accuracy > accuracy:
        accuracy = current_accuracy
        c = current_c
    print(f"Accuracy for C = {current_c}: {current_accuracy}")

print(f"The best accuracy is {accuracy}, C = {c}")

# train final model
final_model = LogisticRegression(C = c)
final_model.fit(X, target)
print(f"Final accuracy is {accuracy_score(target, final_model.predict(X_test))}")

# predict on new review
new_review = ["It was boring movie. It doesn't worth to watch it"]
new_review_clean = preprocess_reviews(new_review)
# cv = CountVectorizer(binary=True)
# cv.fit(reviews_train_clean)
X_new_review = cv.transform(new_review_clean)
y_new_review = final_model.predict(X_new_review)
print(y_new_review)


