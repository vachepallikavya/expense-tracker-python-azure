from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary in-memory storage for expenses
expenses = []

@app.route('/')
def home():
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['POST'])
def add_expense():
    data = request.form
    expense = {
        'name': data.get('name'),
        'amount': data.get('amount')
    }
    expenses.append(expense)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
