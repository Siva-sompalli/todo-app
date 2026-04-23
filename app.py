from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database connection
def get_db():
    return sqlite3.connect("todo.db")

@app.route("/")
def index():
    db = get_db()
    tasks = db.execute("SELECT * FROM tasks").fetchall()
    db.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    task = request.form["task"]
    db = get_db()
    db.execute(
        "INSERT INTO tasks (task, completed) VALUES (?, ?)",
        (task, 0)
    )
    db.commit()
    db.close()
    return redirect("/")

@app.route("/complete/<int:id>")
def complete_task(id):
    db = get_db()
    db.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (id,))
    db.commit()
    db.close()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete_task(id):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", (id,))
    db.commit()
    db.close()
    return redirect("/")

if __name__ == "__main__":
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            completed INTEGER
        )
    """)
    db.commit()
    db.close()

    app.run(debug=True)
