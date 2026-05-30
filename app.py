# Phase 1: the smallest Flask app that can possibly work.


from flask import Flask

# `Flask(__name__)` creates the application object.
#
# `__name__` is a Python built-in that holds the current module's name. When
# this file is run, __name__ == "app" (because the file is app.py)
app = Flask(__name__)


# `@app.route("/")` is a decorator. It tells Flask: "when an HTTP request
# arrives for the path /, call the function below and use whatever it returns
# as the response body."
#
@app.route("/")
def home():

    return "Hello from Flask. Phase 1 is alive."


if __name__ == "__main__":
    app.run(debug=True)
