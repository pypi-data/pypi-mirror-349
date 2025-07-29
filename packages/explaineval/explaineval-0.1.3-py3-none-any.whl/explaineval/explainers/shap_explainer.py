import shap
import matplotlib.pyplot as plt

class ShapExplainer:
    def __init__(self, model, background_data):
        self.model = model
        self.explainer = shap.Explainer(model, background_data)

    def explain(self, X_sample):
        shap_values = self.explainer(X_sample)

        # ✅ Handle multi-class classification
        if isinstance(shap_values, list) or hasattr(shap_values, "__getitem__") and isinstance(shap_values[0].values, (list, tuple)):
            print("⚠️ Multi-class detected. Showing SHAP beeswarm plot for class 0")
            shap.plots.beeswarm(shap_values[0])
        else:
            shap.plots.beeswarm(shap_values)

        plt.show()
