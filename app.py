from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

state_tax_rates = {
    "AZ": 0.0253,
    "CA": 0.09,
    "TX": 0.0,
    "NY": 0.0685,
    "FL": 0.0,
    "CO": 0.044,
    "IL": 0.0495,
    "GA": 0.0575,
    "NC": 0.0475,
    "PA": 0.0307,
}

@app.route("/compare_states", methods=["POST"])
def compare_states():
    data = request.get_json()
    income = data.get("agi", 0)
    state_1 = data.get("state_1")
    state_2 = data.get("state_2")

    def calc_tax(state):
        rate = state_tax_rates.get(state.upper(), 0)
        return round(income * rate, 2)

    return jsonify({
        "state_1": {
            "state": state_1,
            "estimated_tax": calc_tax(state_1)
        },
        "state_2": {
            "state": state_2,
            "estimated_tax": calc_tax(state_2)
        },
        "savings": round(abs(calc_tax(state_1) - calc_tax(state_2)), 2)
    })

@app.route("/", methods=["GET"])
def health_check():
    return "State tax analyzer is live!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
