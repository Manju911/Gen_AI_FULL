from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/leave")
def leave():
    return jsonify({
        "leave_balance": 18
    })

@app.route("/salary")
def salary():
    return jsonify({
        "salary": 85000
    })

@app.route("/attendance")
def attendance():
    return jsonify({
        "attendance": "96%"
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)