
from flask import Flask, request, render_template_string

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Capital Quiz</title>
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
            padding: 20px;
        }

        .quiz-box {
            background: white;
            width: 100%;
            max-width: 450px;
            padding: 30px;
            border-radius: 18px;
            box-shadow: 0 10px 30px #2224;
        }

        h1 {
            text-align: center;
            color: #5b4baf;
        }

        p {
            color: #444;
            font-weight: bold;
            margin-top: 24px;
        }

        input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 16px;
        }

        button {
            width: 100%;
            padding: 13px;
            margin-top: 25px;
            background: #6654d9;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 17px;
            cursor: pointer;
        }

        button:hover {
            background: #4936b5;
        }

        .result {
            margin-top: 20px;
            padding: 12px;
            border-radius: 8px;
            background: #f1f0ff;
            line-height: 1.8;
        }

        .correct {
            color: green;
        }

        .wrong {
            color: red;
        }
    </style>
</head>
<body>
    <div class="quiz-box">
        <h1>🌍 Capital Quiz</h1>
        <p>1. What is the capital of India?</p>
        <p>2. What is the capital of Telangana?</p>

        <form method="POST">
            <input type="text" name="india"
                   placeholder="Enter capital of India"
                   value="{{ india }}" required>

            <input style="margin-top:15px" type="text"
                   name="telangana"
                   placeholder="Enter capital of Telangana"
                   value="{{ telangana }}" required>

            <button type="submit">Check Answers</button>
        </form>

        {% if submitted %}
        <div class="result">
            <div class="{{ 'correct' if india_ok else 'wrong' }}">
                India: {{ 'Correct answer!' if india_ok else
                'Wrong answer! Correct answer: New Delhi' }}
            </div>

            <div class="{{ 'correct' if telangana_ok else 'wrong' }}">
                Telangana: {{ 'Correct answer!' if telangana_ok else
                'Wrong answer! Correct answer: Hyderabad' }}
            </div>

            <h3>Score: {{ score }}/2</h3>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def quiz():
    india = ""
    telangana = ""
    submitted = False
    india_ok = False
    telangana_ok = False
    score = 0

    if request.method == "POST":
        india = request.form.get("india", "").strip()
        telangana = request.form.get("telangana", "").strip()

        india_ok = india.casefold() in ["delhi", "new delhi"]
        telangana_ok = telangana.casefold() == "hyderabad"

        score = int(india_ok) + int(telangana_ok)
        submitted = True

    return render_template_string(
        html,
        india=india,
        telangana=telangana,
        submitted=submitted,
        india_ok=india_ok,
        telangana_ok=telangana_ok,
        score=score
    )

if __name__ == "__main__":
    app.run(debug=True)
