from flask import Flask, render_template, request, redirect

app = Flask(__name__)
expenses = []

@app.route('/')
def index():
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['POST'])
def add_expense():
    expenses.append({
        'name': request.form['name'],
        'amount': request.form['amount']
    })
    return redirect('/')

if __name__ == '__main__':
    app.run()
