from flask import Flask, render_template, request

app = Flask(__name__)

# Core calculator functions
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y != 0:
        return x / y
    else:
        return "Cannot divide by zero"

# Web interface route
@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None
    error = None
    if request.method == 'POST':
        try:
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
            operation = request.form['operation']

            if operation == 'add':
                result = add(num1, num2)
            elif operation == 'subtract':
                result = subtract(num1, num2)
            elif operation == 'multiply':
                result = multiply(num1, num2)
            elif operation == 'divide':
                result = divide(num1, num2)
            else:
                error = "Invalid operation selected."
        except Exception as e:
            error = str(e)

    return render_template('index.html', result=result, error=error)

# REST endpoint for /add
@app.route('/add')
def add_route():
    try:
        x = float(request.args.get('x'))
        y = float(request.args.get('y'))
        return str(add(x, y))
    except Exception as e:
        return f"Error: {str(e)}", 400

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
