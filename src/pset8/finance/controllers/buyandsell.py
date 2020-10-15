# Library imports
from flask import redirect, render_template, request, session

# Local imports
from application import app, db
from helpers import apology, login_required, lookup, usd


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
            return apology(f"sorry... we could not find the \"{symbol}\"", 403)

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
            amount = request.form.get("amount")
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
            return apology(f"sorry... we could not find the \"{symbol}\"", 403)
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
                   total=float(amount * quote_price), user_id=user_id)
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
            amount = request.form.get("amount")
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
            return apology(f"sorry... we could not find the \"{symbol}\"", 403)
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
