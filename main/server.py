from flask import Flask, render_template, request
import os
import psutil

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('Start') == 'Start':
            os.system("python3 main/lightshow.py")
    elif request.method == 'GET':
        return render_template('index.html')

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
