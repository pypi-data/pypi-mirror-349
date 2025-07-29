import shap
import matplotlib.pyplot as plt

class ShapExplainer:
    def __init__(self, model, background_data):
        self.model = model
        self.explainer = shap.Explainer(model, background_data)

    def explain(self, X_sample):
        shap_values = self.explainer(X_sample)

        # 🧠 Check if multi-class and handle it
        if isinstance(shap_values.values, list):
            print("⚠️ Multi-class detected. Showing beeswarm plot for class 0.")
            shap.plots.beeswarm(shap_values[0])  # explain class 0 only
        else:
            shap.plots.beeswarm(shap_values)

        plt.show()
