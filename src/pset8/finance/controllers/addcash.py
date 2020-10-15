# Library imports
from flask import redirect, render_template, request, session

# Local imports
from application import app, db
from helpers import apology, login_required, lookup, usd

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
        db.execute("UPDATE users SET cash = cash + :amount WHERE id=:user_id;", user_id=user_id, amount=amount)
        db.execute("COMMIT;")

        # Redirect to home page
        return redirect("/")

    # Else return addcash.html
    else:
        return render_template("addcash.html")
    