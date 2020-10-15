# Library imports
from flask import redirect, render_template, request, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

# Local imports
from application import app, db
from helpers import apology


def get_user_id_by_username(username):
    """ Gets user id in database. If user exists, returns user id(int) else returns -1"""

    rows = db.execute(
        "SELECT id FROM users WHERE username=:username;", username=username)
    if not rows:
        return -1
    return rows[0]['id']


@app.route("/check", methods=["GET"])
def check():
    # Get arguments
    username = request.args.get("username")

    # Ensure username was submitted
    if not username:
        return apology("must provide username", 403)

    # Check user is exist
    result = True
    if get_user_id_by_username(username) != -1:
        result = False

    # Return result
    return jsonify(result)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get arguments
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get arguments
        username = request.form.get("username")
        password = request.form.get("password")
        password_again = request.form.get("password-again")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password or not password_again:
            return apology("must provide password", 400)

        # Ensure passwords was match
        elif password != password_again:
            return apology("passwords do not match", 403)

        # Check user is exist
        if get_user_id_by_username(username) != -1:
            return apology("username exists")

        # Add new user in database
        db.execute("INSERT INTO users(username, hash, cash) VALUES(:username, :hash, 10000);",
                   username=username,
                   hash=generate_password_hash(password))

        # Add user id in session
        session["user_id"] = db.execute("SELECT id FROM users WHERE username=:username",
                                        username=username)[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
