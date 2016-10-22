from flask import Flask
from flask import render_template
from flask import request, url_for

app = Flask(__name__)

@app.route("/")
def hello(name=None):
    return render_template('main.html', name=name)

@app.route("/main.html")
def main():
    return render_template('main.html', method=['POST'])

@app.route('/contact_form.html')
def client():
	return render_template('contact_form.html')

@app.route('/rcv_form.html')
def recive():
	return render_template('rcv_form.html')

@app.route('/snd_form.html')
def send():
	return render_template('snd_form.html')

if __name__ == "__main__":
    app.run()