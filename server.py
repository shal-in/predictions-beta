from flask import Flask, render_template
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key12"

@app.route("/")
def index():
    return render_template("test.html")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    app.run(debug=True, host='0.0.0.0', port=port)