
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample price table (can be swapped to DB/CSV later)
PRICE_TABLE = {
    "도배(㎡)": 10000,
    "바닥(㎡)": 20000,
    "페인트(㎡)": 8000,
    "조명(개)": 50000
}

@app.route("/")
def index():
    return render_template("index.html", price_table=PRICE_TABLE)

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json or {}
    total = 0
    details = []
    for item, qty in data.items():
        try:
            qty = float(qty)
        except (TypeError, ValueError):
            qty = 0
        if item in PRICE_TABLE and qty > 0:
            unit = PRICE_TABLE[item]
            subtotal = unit * qty
            details.append({"항목": item, "수량": qty, "단가": unit, "금액": subtotal})
            total += subtotal
    return jsonify({"총액": total, "상세": details})

if __name__ == "__main__":
    app.run(debug=True)
