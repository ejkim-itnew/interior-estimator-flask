# app.py 맨 위쪽 import 근처
from flask import Flask, render_template, request, jsonify
import datetime
import os

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

@app.route("/healthz")
def healthz():
    return {
        "ok": True,
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }, 200

# app.py 맨 아래
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    # host=0.0.0.0, port=$PORT 가 핵심
    app.run(host="0.0.0.0", port=port)



