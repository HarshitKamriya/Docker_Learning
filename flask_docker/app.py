from flask import Flask

app = Flask(__name__)



@app.route("/")
def home():
    return "Hello from Docker + Flask 🚀"


@app.route("/about")
def about():
    return {
        "name":"Harshit",
        "technology":"Docker + Flask",
        "status":"Running Successfully"
    }


if __name__=="__main__":
    app.run(host="0.0.0.0",port = 5000)

    





















