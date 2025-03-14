from flask import Flask, request, session, render_template_string, redirect, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Weak secret key

# Reset balance every time app restarts
users = {"john": {"password": "password123", "balance": 1000}}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            session["username"] = username
            return redirect(url_for("dashboard"))

        return "<p class='text-danger text-center'>Invalid credentials!</p>"

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f4f4f4; }
            .login-container { width: 350px; padding: 20px; background: white; box-shadow: 0 0 10px rgba(0,0,0,0.1); border-radius: 10px; }
        </style>
    </head>
    <body>
        <div class="login-container">
            <h3 class="text-center">Login</h3>
            <form method="post">
                <div class="mb-3">
                    <input type="text" name="username" class="form-control" placeholder="Username" required>
                </div>
                <div class="mb-3">
                    <input type="password" name="password" class="form-control" placeholder="Password" required>
                </div>
                <button type="submit" class="btn btn-primary w-100">Login</button>
            </form>
        </div>
    </body>
    </html>
    """)

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    balance = users[username]["balance"]

    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ background-color: #f4f4f4; padding: 40px; }}
            .dashboard-container {{ max-width: 500px; margin: auto; padding: 20px; background: white; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); text-align: center; }}
            .balance {{ font-size: 1.5rem; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="dashboard-container">
            <h2>Welcome, {username}!</h2>
            <p class="balance">Balance: <span class="text-success">${balance}</span></p>
            <a href='/transfer' class="btn btn-warning w-100 mb-2">Transfer Money</a>
            <a href='/reset' class="btn btn-secondary w-100 mb-2">Reset Balance</a>
            <a href='/logout' class="btn btn-danger w-100">Logout</a>
        </div>
    </body>
    </html>
    """)

@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        amount = int(request.form["amount"])
        recipient = request.form["recipient"]

        # Deduct amount only if sufficient balance
        if users[session["username"]]["balance"] >= amount:
            users[session["username"]]["balance"] -= amount
            return f"<p class='text-success text-center'>Transfer Successful! You sent ${amount} to {recipient}.</p>"
        else:
            return "<p class='text-danger text-center'>Insufficient balance!</p>"

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Transfer Money</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f4f4f4; }}
            .transfer-container {{ width: 350px; padding: 20px; background: white; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        </style>
    </head>
    <body>
        <div class="transfer-container">
            <h3 class="text-center">Transfer Money</h3>
            <form method="post">
                <div class="mb-3">
                    <input type="text" name="recipient" class="form-control" placeholder="Recipient" required>
                </div>
                <div class="mb-3">
                    <input type="number" name="amount" class="form-control" placeholder="Amount" required>
                </div>
                <button type="submit" class="btn btn-warning w-100">Send Money</button>
            </form>
        </div>
    </body>
    </html>
    """)

@app.route("/reset")
def reset_balance():
    if "username" in session:
        users[session["username"]]["balance"] = 1000
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
