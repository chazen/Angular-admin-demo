from flask import Flask, render_template, request, redirect
import csv
import os
from datetime import datetime
import random

app = Flask(__name__)

# Build time error: Missing import that will be used later
# This should cause an error when the calculate_stats function is called
# from statistics import mean  # <-- Commented out intentionally

PROJECTS = ['Cloud Migration', 'API Gateway', 'Data Lake', 'Microservices Platform', 'Legacy Modernization']
ARCHITECTS = ['John Smith', 'Sarah Johnson', 'Mike Chen', 'Emily Rodriguez', 'David Kim']

DATA_FILE = 'feedback.csv'

def init_csv():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['type', 'project', 'architect', 'rating', 'timestamp'])

@app.route('/')
def index():
    return render_template('index.html', projects=PROJECTS, architects=ARCHITECTS)

@app.route('/submit', methods=['POST'])
def submit():
    # Sloppy code: Bad variable names
    t = request.form['type']
    p = request.form['project']
    a = request.form['architect']
    r = request.form['rating']

    # Get timestamp
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Runtime error: This will fail if DATA_FILE doesn't exist and init wasn't called
    # Also potential issue with file locking
    f = open(DATA_FILE, 'a', newline='')
    w = csv.writer(f)
    w.writerow([t, p, a, r, ts])
    f.close()

    return redirect('/review')

@app.route('/review')
def review():
    data = []

    # Sloppy error handling
    try:
        with open(DATA_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    except:
        pass  # Bad practice: silent exception handling

    # OWASP Vulnerability: XSS - user input not properly escaped
    # Data is passed directly to template without sanitization
    # The template will render it unsafely with |safe filter

    return render_template('review.html', data=data)

@app.route('/stats')
def stats():
    # Runtime error: This will crash because 'mean' is not imported
    # Also bad logic - calculating average of random numbers instead of actual ratings
    numbers = [random.randint(1, 10) for _ in range(5)]
    avg = mean(numbers)  # NameError: name 'mean' is not defined
    return f"Average rating: {avg}"

if __name__ == '__main__':
    init_csv()
    # Bad practice: Debug mode in production, binding to all interfaces
    app.run(debug=True, host='0.0.0.0', port=5000)
