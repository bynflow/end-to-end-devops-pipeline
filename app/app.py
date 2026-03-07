from flask import Flask, request, render_template
import os


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        expr = request.form.get('number', '')
        if not expr.isdigit():
            return render_template('number_square.html', error="Please enter a valid non-negative integer.")
        result = int(expr) ** 2
        return render_template('result.html',
                               number=expr,
                               square=result,
                               container_name=os.environ.get("CONTAINER_NAME", "unknown"),
                               public_ip=os.environ.get("PUBLIC_IP", "unknown"))
    return render_template('number_square.html')

@app.get("/health")
def health():
    return {"status":"ok"}, 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
