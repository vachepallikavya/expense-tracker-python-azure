from flask import Flask, render_template, request, redirect, make_response
from datetime import datetime

app = Flask(__name__)
expenses = []

@app.route('/')
def index():
    # Create category totals for pie chart
    category_totals = {}
    for expense in expenses:
        category = expense['item_type']
        category_totals[category] = category_totals.get(category, 0) + float(expense['amount'])

    labels = list(category_totals.keys())
    data = list(category_totals.values())

    return render_template('index.html', expenses=expenses, labels=labels, data=data)

@app.route('/add', methods=['POST'])
def add_expense():
    name = request.form.get('name')
    amount = request.form.get('amount')
    item_type = request.form.get('item_type')
    payment_type = request.form.get('payment_type')

    if name and amount and item_type:
        expenses.append({
            'sn': len(expenses) + 1,
            'name': name,
            'amount': float(amount),
            'item_type': item_type,
            'payment_type': payment_type,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return redirect('/')

# ✅ Export CSV feature
@app.route('/export')
def export_csv():
    def generate():
        data = ["S.N,Name,Amount,Category,Payment Type,Date\n"]
        for e in expenses:
            data.append(f"{e['sn']},{e['name']},{e['amount']},{e['item_type']},{e['payment_type']},{e['date']}\n")
        return "".join(data)

    response = make_response(generate())
    response.headers["Content-Disposition"] = "attachment; filename=expenses.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

@app.route('/test')
def test():
    return "<h1>Hello Flask!</h1>"

if __name__ == '__main__':
    app.run(debug=True)



