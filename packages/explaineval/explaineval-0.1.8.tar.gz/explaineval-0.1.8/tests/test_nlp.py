from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from explaineval.main import EvalX

def test_nlp():
    texts = ["I love apples", "You hate bananas", "He loves mangoes", "She dislikes grapes"]
    labels = [1, 0, 1, 0]
    model = Pipeline([
        ("vec", CountVectorizer()),
        ("clf", MultinomialNB())
    ]).fit(texts, labels)

    evalx = EvalX(model, task="nlp", background_data=texts)
    metrics = evalx.evaluate(texts, labels)
    evalx.generate_report("nlp_report.html")
    assert "accuracy" in metrics
