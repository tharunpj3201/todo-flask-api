
import sqlite3
from flask import Flask,jsonify,request,render_template

app=Flask(__name__)

def get_db():
    return sqlite3.connect("todo.db")

@app.route("/ui")
def ui():
    return render_template("index.html")

@app.route("/",methods=["POST","GET"])
def home():
    return "Todo API is running"

@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.json
    title = data.get("title")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO todos (title, completed) VALUES (?, ?)",
        (title, 0)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Todo added successfully"}), 201


@app.route("/todos", methods=["GET"])
def get_todos():
    conn = get_db()
    cur = conn.cursor()

    rows = cur.execute(
        "SELECT id, title, completed FROM todos"
    ).fetchall()

    conn.close()

    todos = []
    for row in rows:
        todos.append({
            "id": row[0],
            "title": row[1],
            "completed": row[2]
        })

    return jsonify(todos)

@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.json
    title = data.get("title")
    completed = data.get("completed")

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE todos SET title = ?, completed = ? WHERE id = ?",
        (title, completed, todo_id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Todo updated successfully"})


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM todos WHERE id = ?",
        (todo_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Todo deleted successfully"})

if __name__=="__main__":
    app.run(debug=True)