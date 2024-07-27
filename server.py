from flask import Flask, render_template
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key12"

file_path = "text.txt"

if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
else:
    content = os.getenv('TEXT_CONTENT', 'Default text if ENV variable is not set')

print(content)


@app.route("/")
def index():
    return render_template("test.html")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    app.run(debug=True, host='0.0.0.0', port=port)