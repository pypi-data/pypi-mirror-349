import shap
import matplotlib.pyplot as plt

class ShapExplainer:
    def __init__(self, model, background_data):
        self.model = model
        self.is_pipeline = hasattr(model, "predict_proba") is False and hasattr(model, "steps")
        self.explainer = None

        if self.is_pipeline:
            vec = model.named_steps["vec"]
            clf = model.named_steps["clf"]
            background_matrix = vec.transform(background_data)
            self.explainer = shap.Explainer(clf.predict_proba, background_matrix)
            self.vectorizer = vec
        else:
            self.explainer = shap.Explainer(model, background_data)

    def explain(self, X_sample):
        if self.is_pipeline:
            X_sample_vec = self.vectorizer.transform(X_sample)
            shap_values = self.explainer(X_sample_vec)
        else:
            shap_values = self.explainer(X_sample, check_additivity=False)

        if hasattr(shap_values, "values") and len(shap_values.values.shape) == 3:
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
