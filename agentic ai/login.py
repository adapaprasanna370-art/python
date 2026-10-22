
from flask import Flask, request, render_template_string

app = Flask(__name__)

correct_password = "1234"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Login</title>
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #141e30, #243b55);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .login-box {
            background: white;
            padding: 40px;
            width: 350px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 30px #0005;
        }

        h1 {
            color: #243b55;
            margin-bottom: 10px;
        }

        p {
            color: #666;
        }

        input {
            width: 100%;
            padding: 13px;
            margin: 20px 0;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 16px;
        }

        button {
            width: 100%;
            padding: 13px;
            background: #243b55;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background: #141e30;
        }

        .message {
            margin-top: 20px;
            font-weight: bold;
        }

        .success { color: green; }
        .error { color: red; }
        .locked { color: darkred; }
    </style>
</head>
<body>
    <div class="login-box">
        <h1>Welcome Back</h1>
        <p>Enter your password to continue</p>

        <form method="POST">
            <input type="password" name="password"
                   placeholder="Enter your password" required>
            <button type="submit">Login</button>
        </form>

        <div class="message {{ status }}">
            {{ message }}
        </div>

        {% if attempts < 3 and not success %}
            <p>Attempts remaining: {{ 3 - attempts }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

attempts = 0
locked = False
success = False

@app.route("/", methods=["GET", "POST"])
def login():
    global attempts, locked, success

    message = ""
    status = ""

    if request.method == "POST":
        if locked:
            message = "Account locked!"
            status = "locked"

        elif success:
            message = "You are already logged in!"
            status = "success"

        else:
            password = request.form.get("password", "")

            if password == correct_password:
                success = True
                message = "Login successful!"
                status = "success"
            else:
                attempts += 1

                if attempts >= 3:
                    locked = True
                    message = "Account locked after 3 attempts!"
                    status = "locked"
                else:
                    message = "Wrong password!"
                    status = "error"

    return render_template_string(
        HTML,
        message=message,
        status=status,
        attempts=attempts,
        success=success
    )

if __name__ == "__main__":
    app.run(debug=True)
