from flask import Flask, render_template, request, redirect
from collections import defaultdict

app = Flask(__name__)
expenses = []

@app.route('/', methods=['GET', 'POST'])
def index():
    filtered = expenses

    # Handle filters
    if request.method == 'GET':
        date = request.args.get('date')
        category = request.args.get('category')
        payment_type = request.args.get('payment_type')

        if date:
            filtered = [e for e in filtered if e['date'] == date]
        if category and category != "All":
            filtered = [e for e in filtered if e['category'] == category]
        if payment_type and payment_type != "All":
            filtered = [e for e in filtered if e['payment'] == payment_type]

    # Dashboard Summary: Category totals for pie chart
    category_totals = defaultdict(float)
    for e in filtered:
        category_totals[e['category']] += float(e['amount'])

    chart_labels = list(category_totals.keys())
    chart_values = list(category_totals.values())

    return render_template(
        'index.html',
        expenses=filtered,
        chart_labels=chart_labels,
        chart_values=chart_values
    )

@app.route('/add', methods=['POST'])
def add_expense():
    name = request.form.get('name')
    amount = request.form.get('amount')
    category = request.form.get('category')
    payment = request.form.get('payment')
    date = request.form.get('date')

    if name and amount and category and payment and date:
        expenses.append({
            'sn': len(expenses) + 1,
            'name': name,
            'amount': amount,
            'category': category,
            'payment': payment,
            'date': date
        })

    return redirect('/')

@app.route('/test')
def test():
    return "<h1>Hello Flask!</h1>"

if __name__ == '__main__':
    app.run(debug=True)




