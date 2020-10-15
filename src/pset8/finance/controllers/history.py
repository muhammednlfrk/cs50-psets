# Library imports
from flask import render_template, session

# Local imports
from application import app, db
from helpers import login_required, usd


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
