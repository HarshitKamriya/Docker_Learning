from flask import Flask
from flask import request
from database import get_connection
from init_db import initialize_database

app = Flask(__name__)

initialize_database()
@app.route("/")
def home():
    return "Flask + PostgreSQL + Docker"


@app.route("/health")
def health():
    return {
        "status":"UP",
        "message":"Application is running"
    },200





@app.route("/users", methods=["GET"])
def get_users():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")

    users = cur.fetchall()

    cur.close()
    conn.close()

    data = []

    for user in users:
        data.append({
            "id": user[0],
            "name": user[1]
        })

    return data


@app.route("/users", methods=["POST"])
def add_user():

    data = request.get_json()

    if not data or "name" not in data:
        return {
            "error":"Name is required"
        },400

    name = data["name"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users(name) VALUES(%s)",
        (name,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message":"User Added Successfully"
    },201


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM users WHERE id=%s RETURNING id",
        (user_id,)
    )

    deleted = cur.fetchone()

    if deleted is None:
        conn.rollback()
        cur.close()
        conn.close()

        return {
            "error": "User not found"
        },404

    conn.commit()


if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)