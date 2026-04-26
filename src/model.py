import os
import joblib
import mlflow
from mlflow.tracking import MlflowClient

class Model:
    def __init__(self):
        self.model = None
        self.transform_pipeline = None
        # On définit l'adresse du serveur MLflow
        mlflow.set_tracking_uri(os.getenv("MLFLOW_SERVER"))
        self.load_model()

    def load_model(self):
        client = MlflowClient()
        alias = os.getenv("ENV")
        model_name = os.getenv("MLFLOW_REGISTRY_NAME")

        # 1. Récupérer la version du modèle qui a le tag 'staging'
        model_version = client.get_model_version_by_alias(model_name, alias)

        # 2. Télécharger le pipeline de transformation depuis les artifacts du run
        artifact_uri = f"runs:/{model_version.run_id}/transform_pipeline.pkl"
        pipeline_path = mlflow.artifacts.download_artifacts(artifact_uri=artifact_uri)
        
        # On charge le dictionnaire d'encodeurs
        self.transform_pipeline = joblib.load(pipeline_path)

        # 3. Charger le modèle LightGBM
        self.model = mlflow.sklearn.load_model(f"models:/{model_name}@{alias}")
        print(f"✅ Modèle et Pipeline chargés (Version {model_version.version})")

    def predict(self, X):
        # On applique les LabelEncoders sur les données entrantes
        for name, encoder in self.transform_pipeline.items():
            if name in X.columns:
                X[name] = X[name].astype("string").fillna("unknown")
                X[name] = encoder.transform(X[name])
        
        # On retire les colonnes inutiles si elles sont présentes
        X = X.drop(columns=["user_id", "user_session"], errors="ignore")
        
        return self.model.predict(X)