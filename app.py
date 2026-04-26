import pandas as pd
from flask import Flask, request, jsonify
from src.model import Model
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
model = Model()

@app.route("/", methods=["GET"])
def home():
    return "L'API  est en ligne ! ✅", 200

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # On reçoit du JSON
        data = request.get_json()
        # On transforme en DataFrame pandas
        df = pd.read_json(data)
        # On lance la prédiction
        preds = model.predict(df)
        # On renvoie le résultat (converti en liste simple)
        return jsonify(preds.flatten().tolist()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)