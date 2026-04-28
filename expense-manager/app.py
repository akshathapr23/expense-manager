from flask import Flask, render_template, request, jsonify, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"


def get_db():
    return sqlite3.connect("database.db")


def init_db():
    conn = get_db()

    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            category TEXT,
            date TEXT,
            note TEXT
        )
    ''')

    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


# 🔐 REGISTER
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    conn = get_db()

    conn.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (data["username"], data["password"])
    )

    conn.commit()
    conn.close()
    return jsonify({"message": "registered"})


# 🔐 LOGIN
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = get_db()

    cursor = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (data["username"], data["password"])
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        session["user_id"] = user[0]
        return jsonify({"message": "success"})
    else:
        return jsonify({"message": "invalid"})


# ➕ ADD EXPENSE
@app.route("/add", methods=["POST"])
def add_expense():
    if "user_id" not in session:
        return jsonify({"error": "not logged in"})

    data = request.json
    conn = get_db()

    conn.execute(
        "INSERT INTO expenses (user_id, amount, category, date, note) VALUES (?, ?, ?, ?, ?)",
        (session["user_id"], data["amount"], data["category"], data["date"], data["note"])
    )

    conn.commit()
    conn.close()
    return jsonify({"message": "added"})


# 📋 GET EXPENSES
@app.route("/get")
def get_expenses():
    if "user_id" not in session:
        return jsonify([])

    conn = get_db()

    cursor = conn.execute(
        "SELECT * FROM expenses WHERE user_id=?",
        (session["user_id"],)
    )

    data = [
        {"id": row[0], "amount": row[2], "category": row[3], "date": row[4], "note": row[5]}
        for row in cursor.fetchall()
    ]

    conn.close()
    return jsonify(data)


# ❌ DELETE
@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_expense(id):
    conn = get_db()
    conn.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "deleted"})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)