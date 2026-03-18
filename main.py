from flask import Flask, render_template

app = Flask(__name__)

# ────────────────────────────── ROUTES ──────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/allcsont-ortopedia')
def allcsont_ortopedia():
    return render_template('allcsont_ortopedia.html')

@app.route('/orvosaink')
def orvosaink():
    return render_template('orvosaink.html')

@app.route('/kapcsolat')
def kapcsolat():
    return render_template('contact.html')

# Optional: redirect old path
@app.route('/allcsont-ortopedia')
def old_path():
    return render_template('allcsont_ortopedia.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
