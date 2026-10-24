
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Demo nutrition values per 100 grams.
# These are approximate illustrative values.
DEMO_DATA = {
    "egg": {"calories": 155, "protein": 13, "carbs": 1.1, "fat": 11},
    "chicken": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6},
    "apple": {"calories": 52, "protein": 0.3, "carbs": 13.8, "fat": 0.2},
    "rice": {"calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3},
    "banana": {"calories": 89, "protein": 1.1, "carbs": 22.8, "fat": 0.3},
}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Nutrition Checker</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #eef5f0;
            color: #24352b;
        }
        .container {
            max-width: 520px;
            margin: 60px auto;
            padding: 30px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 8px 25px #0001;
        }
        h1 { text-align: center; color: #218653; }
        p { text-align: center; color: #647267; }
        input, button {
            width: 100%;
            padding: 13px;
            margin-top: 12px;
            border-radius: 8px;
            font-size: 16px;
        }
        input { border: 1px solid #b9c9be; }
        button {
            border: none;
            background: #218653;
            color: white;
            cursor: pointer;
        }
        button:hover { background: #17663e; }
        .result {
            background: #f0f8f2;
            margin-top: 22px;
            padding: 18px;
            border-radius: 10px;
        }
        .error { color: #b42318; }
        li { padding: 6px; }
        small { color: #66766b; }
    </style>
</head>
<body>
<div class="container">
    <h1>🥗 Nutrition Checker</h1>
    <p>Enter a food to check its demo nutrition values.</p>

    <form method="POST">
        <input name="food" placeholder="Try chicken, egg, apple..."
               value="{{ food }}" required>
        <button type="submit">Check Nutrition</button>
    </form>

    {% if data %}
    <div class="result">
        <h2>{{ food.title() }}</h2>
        <small>Approximate values per 100 grams</small>
        <ul>
            <li>Calories: {{ data.calories }} kcal</li>
            <li>Protein: {{ data.protein }} g</li>
            <li>Carbohydrates: {{ data.carbs }} g</li>
            <li>Fat: {{ data.fat }} g</li>
        </ul>
    </div>
    {% endif %}

    {% if error %}
    <div class="result error">{{ error }}</div>
    {% endif %}
    <p><small>Demo data only. Actual nutrition varies by food and preparation.</small></p>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    food = ""
    data = None
    error = ""

    if request.method == "POST":
        food = request.form.get("food", "").strip().lower()
        data = DEMO_DATA.get(food)

        if not data:
            error = (
                "Food not in demo data. Try: egg, chicken, "
                "apple, rice, or banana."
            )

    return render_template_string(
        HTML, food=food, data=data, error=error
    )

if __name__ == "__main__":
    app.run(debug=True)
