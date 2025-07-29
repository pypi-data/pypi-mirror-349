from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from explaineval.main import EvalX

def test_regression():
    X, y = load_diabetes(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestRegressor().fit(X_train, y_train)

    evalx = EvalX(model, task='regression', background_data=X_train)
    metrics = evalx.evaluate(X_test, y_test)
    evalx.explain(X_test[:5])
    evalx.generate_report("regression_report.html")
    assert "RMSE" in metrics
