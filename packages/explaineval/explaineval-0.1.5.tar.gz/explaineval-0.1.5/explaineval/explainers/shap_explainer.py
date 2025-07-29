import shap
import matplotlib.pyplot as plt

class ShapExplainer:
    def __init__(self, model, background_data):
        self.model = model
        self.explainer = shap.Explainer(model, background_data)

    def explain(self, X_sample):
        shap_values = self.explainer(X_sample)

        # ✅ Handle 3D output (multi-class SHAP)
        if len(shap_values.values.shape) == 3:
            print("⚠️ Detected multi-class SHAP output. Showing class 0")
            shap.plots.beeswarm(shap.Explanation(
                values=shap_values.values[:, :, 0],
                base_values=shap_values.base_values[:, 0],
                data=shap_values.data,
                feature_names=shap_values.feature_names
            ))
        else:
            shap.plots.beeswarm(shap_values)

        plt.show()

