from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello from Git+Docker+Jenkins!!! And Here's the CI/CD pipeline"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
