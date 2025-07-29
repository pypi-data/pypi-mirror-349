import numpy as np
from sklearn.ensemble import RandomForestRegressor
from explaineval.main import EvalX

def test_timeseries():
    X = np.array([[i, i+1, i+2] for i in range(100)])
    y = np.array([i+3 for i in range(100)])
    model = RandomForestRegressor().fit(X[:80], y[:80])

    evalx = EvalX(model, task="timeseries", background_data=X[:80])
    metrics = evalx.evaluate(X[80:], y[80:])
    evalx.generate_report("timeseries_report.html")
    assert "MAE" in metrics
