from explaineval.main import EvalX
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

import sys
import os

# Add the parent directory to Python path BEFORE importing explaineval
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_classification():
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestClassifier().fit(X_train, y_train)

    evalx = EvalX(model, task='classification', background_data=X_train)
    metrics = evalx.evaluate(X_test, y_test)
    evalx.explain(X_test[:5])
    evalx.generate_report("classification_report.html")
    assert "accuracy" in metrics


if __name__ == "__main__":
    test_classification()
