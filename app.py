from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'instance', 'expenses.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Expense model
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
    return render_template('index.html', expenses=expenses)

# Route to add a new expense
@app.route('/add', methods=['POST'])
def add_expense():
    category = request.form['category']
    description = request.form['description']
    amount = float(request.form['amount'])
    payment_method = request.form['payment_method']

    new_expense = Expense(category=category, description=description, amount=amount, payment_method=payment_method)
    db.session.add(new_expense)
    db.session.commit()
    return redirect(url_for('index'))

# Route to delete an expense
@app.route('/delete/<int:id>')
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('index'))

# Main entry point
if __name__ == "__main__":
    app.run(debug=True)
