import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# ---------------------------
# App setup
# ---------------------------
def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///expenses.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    return app

app = create_app()
db = SQLAlchemy(app)

# ---------------------------
# Database model
# ---------------------------
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    payment_method = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"<Expense {self.id} {self.category} {self.amount}>"

# ---------------------------
# Routes
# ---------------------------
@app.route("/", methods=["GET"])
def index():
    # Filters
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    category = request.args.get("category")

    query = Expense.query
    if start_date:
        try:
            sd = datetime.strptime(start_date, "%Y-%m-%d").date()
            query = query.filter(Expense.date >= sd)
        except ValueError:
            flash("Invalid start date format. Use YYYY-MM-DD", "error")
    if end_date:
        try:
            ed = datetime.strptime(end_date, "%Y-%m-%d").date()
            query = query.filter(Expense.date <= ed)
        except ValueError:
            flash("Invalid end date format. Use YYYY-MM-DD", "error")
    if category:
        query = query.filter(Expense.category.ilike(f"%{category}%"))

    expenses = query.order_by(Expense.date.desc(), Expense.id.desc()).all()
    total = sum(e.amount for e in expenses)
    return render_template("index.html", expenses=expenses, total=total)

@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        try:
            date_str = request.form.get("date") or datetime.utcnow().strftime("%Y-%m-%d")
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            category = (request.form["category"] or "General").strip()
            description = request.form.get("description", "").strip()
            amount = float(request.form["amount"])
            payment_method = request.form.get("payment_method", "").strip()

            exp = Expense(date=date, category=category, description=description, amount=amount, payment_method=payment_method)
            db.session.add(exp)
            db.session.commit()
            flash("Expense added!", "success")
            return redirect(url_for("index"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding expense: {e}", "error")
    return render_template("add_expense.html")

@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):
    exp = Expense.query.get_or_404(expense_id)
    if request.method == "POST":
        try:
            date_str = request.form.get("date") or exp.date.strftime("%Y-%m-%d")
            exp.date = datetime.strptime(date_str, "%Y-%m-%d").date()
            exp.category = (request.form["category"] or exp.category).strip()
            exp.description = request.form.get("description", "").strip()
            exp.amount = float(request.form["amount"])
            exp.payment_method = request.form.get("payment_method", "").strip()
            db.session.commit()
            flash("Expense updated!", "success")
            return redirect(url_for("index"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating expense: {e}", "error")
    return render_template("edit_expense.html", exp=exp)

@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    exp = Expense.query.get_or_404(expense_id)
    try:
        db.session.delete(exp)
        db.session.commit()
        flash("Expense deleted.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting expense: {e}", "error")
    return redirect(url_for("index"))

# ---------------------------
# CLI command to init database
# ---------------------------
@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
    print("Database initialized")

# ---------------------------
# Run the app
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
