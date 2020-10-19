# Library imports
import sys
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Local imports
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

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
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password or not confirmation:
            return apology("must provide password", 400)

        # Ensure passwords was match
        elif password != confirmation:
            return apology("passwords do not match", 400)

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


@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    """Add cash in the user account"""

    # If POST request, add cash on the user account
    if request.method == "POST":
        # Get arguments
        user_id = session["user_id"]
        amount = request.form.get("amount")

        # Ensure amount was submitted
        if not amount:
            return apology("amount is not submitted", 400)

        # Update data in db
        db.execute("BEGIN TRANSACTION;")
        db.execute("UPDATE users SET cash = cash + :amount WHERE id=:user_id;",
                   user_id=user_id, amount=amount)
        db.execute("COMMIT;")

        # Redirect to home page
        return redirect("/")

    # Else return addcash.html
    else:
        return render_template("addcash.html")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure symbol was submitted
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)

        # Get quote value
        quote = lookup(symbol)

        # Return a apology if quote not find
        if not quote:
            return apology(f"sorry... we could not find the \"{symbol}\"", 400)

        # Format data
        quote["price"] = usd(quote["price"])

        # Redirect user to home page
        return render_template("quoted.html", quote=quote)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get arguments
        user_id = session["user_id"]
        symbol = request.form.get("symbol")
        amount = ""
        try:
            amount = request.form.get("shares")
            if not amount:
                return apology("must provide shares count", 400)
            amount = int(amount)
        except:
            return apology("shares count is not valid", 400)

        # Ensure symbol was submitted
        if not symbol:
            return apology("must provide symbol", 400)

        # Ensure shares count was grather than 0
        elif amount < 1:
            return apology("shares count not grather than 0", 400)

        # Check symbol is valid, get shares name and get shares price
        quote = lookup(symbol)
        if not quote:
            return apology(f"sorry... we could not find the \"{symbol}\"", 400)
        symbol = quote["symbol"]
        quote_price = quote["price"]

        # Check user cash
        cash = float(db.execute(
            "SELECT cash FROM users WHERE id=:user_id", user_id=user_id)[0]["cash"])
        if (amount * quote_price) > cash:
            return apology("cash is not enougth")

        # Update user cash and insert new buy operation in database
        db.execute("BEGIN TRANSACTION;")
        db.execute("UPDATE users SET cash = cash - :total WHERE id=:user_id;",
                total=amount * quote_price, user_id=user_id)
        db.execute("INSERT INTO history(user_id, operation, symbol, amount, price) VALUES(:user_id, 1, :symbol, :amount, :price);",
                user_id=user_id, symbol=symbol, amount=amount, price=quote_price)
        db.execute("INSERT INTO shares(user_id, symbol, amount) VALUES(:user_id, :symbol, :amount);",
                user_id=user_id, symbol=symbol, amount=amount)
        db.execute("COMMIT;")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    # Get user_id
    user_id = session["user_id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get arguments
        symbol = request.form.get("symbol")
        amount = ""
        try:
            amount = request.form.get("shares")
            if not amount:
                return apology("must provide shares count", 400)
            amount = int(amount)
        except:
            return apology("shares count is not valid", 400)

        # Ensure symbol was submitted
        if not symbol:
            return apology("must provide symbol", 400)

        # Ensure shares count was grather than 0
        elif amount < 1:
            return apology("shares count not grather than 0", 400)

        # Get and check shares information
        shares = db.execute(
            "SELECT symbol, SUM(amount) AS amount FROM shares WHERE LOWER(symbol)=LOWER(:symbol) GROUP BY symbol LIMIT 1;", symbol=symbol)[0]
        if shares["amount"] < amount:
            return apology(f"unfortunately you don't have \"{amount}\" share", 403)
        shares_total_amount = shares["amount"]
        new_amount = shares_total_amount - amount

        # Check symbol is valid, get shares name and get shares price
        quote = lookup(symbol)
        if not quote:
            return apology(f"sorry... we could not find the \"{symbol}\"", 400)
        quote_price = quote["price"]
        new_total_price = amount * quote_price

        # Update data
        db.execute("BEGIN TRANSACTION;")
        db.execute("UPDATE users SET cash = cash + :total_price WHERE id=:id;",
                   total_price=new_total_price, id=user_id)
        db.execute("INSERT INTO history(user_id, operation, symbol, amount, price) VALUES(:user_id, 2, :symbol, :amount, :price);",
                   user_id=user_id, symbol=symbol, amount=amount, price=quote_price)
        if new_amount == 0:
            db.execute("DELETE FROM shares WHERE symbol=:symbol AND user_id=:user_id;",
                       symbol=symbol, user_id=user_id)
        else:
            db.execute("UPDATE shares SET amount=:new_amount WHERE id IN (SELECT id FROM shares WHERE user_id=:user_id AND LOWER(symbol)=LOWER(:symbol) LIMIT 1);",
                       new_amount=new_amount, user_id=user_id, symbol=symbol)
        db.execute("COMMIT;")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        rows = db.execute(
            "SELECT symbol, SUM(amount) AS amount FROM shares WHERE user_id=:user_id GROUP BY symbol", user_id=user_id)
        symbols = [row["symbol"] for row in rows if row["amount"] > 0]
        return render_template("sell.html", symbols=symbols)


@app.route("/history")
@login_required
def history():
    # Get user_id
    user_id = session["user_id"]

    # Get history
    history = db.execute(
        "SELECT symbol, (CASE operation WHEN 2 THEN (-1 * amount) ELSE amount END) AS amount, price, time FROM history WHERE user_id=:user_id ORDER BY time;",
        user_id=user_id)

    # Fomat data
    for h in history:
        h["price"] = usd(h["price"])

    # Render history page
    return render_template("history.html", rows=history)


@app.route("/")
@login_required
def index():
    """Load index page"""

    # Get arguments
    user_id = session.get("user_id")

    # Get data in database
    shares = db.execute(
        "SELECT symbol, SUM(amount) AS amount FROM shares WHERE user_id=:user_id GROUP BY LOWER(symbol) ORDER BY symbol",
        user_id=user_id)
    cash = db.execute(
        "SELECT cash FROM users WHERE id=:user_id LIMIT 1;",
        user_id=user_id)[0]["cash"]
    total = cash

    # Format data
    for share in shares:
        uptodateshare = lookup(share["symbol"])
        share["price"] = uptodateshare["price"]
        share["total"] = share["price"] * share["amount"]
        total += share["total"]
        share["price"] = usd(share["price"])
        share["total"] = usd(share["total"])
        share["name"] = uptodateshare["name"]
    total = usd(total)
    cash = usd(cash)

    # Return home page
    return render_template("index.html", shares=shares, cash=cash, total=total)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
