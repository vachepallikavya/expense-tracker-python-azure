from flask import Flask, render_template, request, redirect

app = Flask(__name__)
expenses = []

@app.route('/')
def index():
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['POST'])
def add_expense():
    name = request.form.get('name')
    amount = request.form.get('amount')
    if name and amount:
        expenses.append({
            'name': name,
            'amount': amount
        })
    return redirect('/')
@app.route('/test')
def test():
    return "<h1>Hello Flask!</h1>"


if __name__ == '__main__':
    app.run(debug=True)


