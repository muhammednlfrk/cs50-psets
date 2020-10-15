# Library imports
from flask import redirect, render_template, request, session

# Local imports
from application import app, db
from helpers import apology, login_required, lookup, usd


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
