from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "instance")
os.makedirs(db_path, exist_ok=True)  # Ensure instance folder exists
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(db_path, 'expenses.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db = SQLAlchemy(app)

# Expense model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50))

# Home route
@app.route('/')
def index():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    total = sum(e.amount or 0 for e in expenses)
    return render_template('index.html', expenses=expenses, total=total)

# Add expense
@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        category = request.form['category']
        description = request.form['description']
        amount = float(request.form['amount'])
        payment_method = request.form['payment_method']

        new_expense = Expense(
            category=category,
            description=description,
            amount=amount,
            payment_method=payment_method
        )
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_expense.html')

# Edit expense
@app.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if request.method == 'POST':
        expense.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        expense.category = request.form['category']
        expense.description = request.form['description']
        expense.amount = float(request.form['amount'])
        expense.payment_method = request.form['payment_method']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_expense.html', expense=expense)

# Delete expense
@app.route('/delete/<int:expense_id>', methods=['POST', 'GET'])
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('index'))

# Run locally or on Azure
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
