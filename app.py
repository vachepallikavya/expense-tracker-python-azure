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
    item_type = request.form.get('item_type')
    
    if name and amount and item_type:
        expenses.append({
            'sn': len(expenses) + 1,
            'name': name,
            'amount': amount,
            'item_type': item_type
        })
    
    return redirect('/')

@app.route('/test')
def test():
    return "<h1>Hello Flask!</h1>"


if __name__ == '__main__':
    app.run(debug=True)


