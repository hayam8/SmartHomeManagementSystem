from flask import Flask
app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello World!"
@app.route("/test")
def test():
    return "test World!"

if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0', port = '80')