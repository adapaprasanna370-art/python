
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Login details
inbuilt_user_name = "admin"
inbuilt_user_password = "adimin123"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Login</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #e9efff, #f8f9ff);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            display: flex;
            max-width: 900px;
            width: 100%;
            min-height: 510px;
            background: white;
            border-radius: 22px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(35, 55, 100, 0.15);
        }

        .left {
            flex: 1;
            padding: 55px 40px;
            color: white;
            background: linear-gradient(145deg, #183cbe, #7256e8);
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .left h1 {
            font-size: 38px;
            line-height: 1.2;
            margin-bottom: 20px;
        }

        .left p {
            line-height: 1.8;
            color: #e3e7ff;
        }

        .icon {
            font-size: 55px;
            margin-bottom: 28px;
        }

        .right {
            flex: 1;
            padding: 55px 40px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .right h2 {
            color: #202a44;
            font-size: 30px;
            margin-bottom: 10px;
        }

        .subtitle {
            color: #7c8498;
            margin-bottom: 30px;
        }

        label {
            display: block;
            margin: 17px 0 8px;
            color: #303950;
            font-weight: bold;
            font-size: 14px;
        }

        input {
            width: 100%;
            padding: 14px;
            border: 1px solid #dce1ee;
            border-radius: 10px;
            font-size: 15px;
            outline: none;
        }

        input:focus {
            border-color: #5c59e8;
            box-shadow: 0 0 0 3px #eeedff;
        }

        button {
            width: 100%;
            margin-top: 25px;
            padding: 15px;
            border: none;
            border-radius: 10px;
            background: #514be5;
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }

        button:hover {
            background: #3933bd;
            transform: translateY(-2px);
        }

        .message {
            margin-top: 20px;
            padding: 13px;
            border-radius: 9px;
            text-align: center;
            font-size: 14px;
        }

        .success {
            background: #e4f8eb;
            color: #167541;
        }

        .error {
            background: #ffebeb;
            color: #c62828;
        }

        .footer {
            text-align: center;
            color: #8a91a3;
            font-size: 12px;
            margin-top: 25px;
        }

        @media (max-width: 650px) {
            .container {
                flex-direction: column;
            }

            .left, .right {
                padding: 35px 25px;
            }

            .left h1 {
                font-size: 30px;
            }
        }
    </style>
</head>

<body>
    <div class="container">

        <div class="left">
            <div class="icon">🔐</div>
            <h1>Welcome to Your Secure Space</h1>
            <p>
                Sign in to continue. Your workspace is just
                one step away. Enter your credentials to get started.
            </p>
        </div>

        <div class="right">
            <h2>Login</h2>
            <p class="subtitle">Enter your account details below.</p>

            <form method="POST">
                <label for="username">Username</label>
                <input type="text" id="username" name="username"
                       placeholder="Enter your username" required>

                <label for="password">Password</label>
                <input type="password" id="password" name="password"
                       placeholder="Enter your password" required>

                <button type="submit">Sign In →</button>
            </form>

            {% if message %}
                <div class="message {{ status }}">
                    {{ message }}
                </div>
            {% endif %}

            <div class="footer">
                © 2026 Secure Login. All rights reserved.
            </div>
        </div>

    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    status = ""

    if request.method == "POST":
        user_name = request.form.get("username", "")
        user_password = request.form.get("password", "")

        if (user_name == inbuilt_user_name and
                user_password == inbuilt_user_password):
            message = "Login successful! Welcome, admin."
            status = "success"
        else:
            message = "Invalid username or password."
            status = "error"

    return render_template_string(
        HTML, message=message, status=status
    )

if __name__ == "__main__":
    app.run(debug=True)
