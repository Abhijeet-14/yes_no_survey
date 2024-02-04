from flask import Flask, request, redirect, url_for, jsonify
import logging

logger = logging.getLogger(__name__)
# import sqlite3

app = Flask(__name__)

# Database setup
# DATABASE = "example.db"

# def create_table():
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS tasks (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             title TEXT NOT NULL,
#             description TEXT
#         )
#     ''')
#     conn.commit()
#     conn.close()

DB = {}


def create_db():
    print("creating db")
    return {"question": "", "answer": {"yes": 0, "no": 0}}


def check_question_exist():
    if not DB.get("question"):
        raise Exception("No survey exist, please create a new one.")


@app.route("/generate", methods=["POST"])
def create_question():
    if request.method == "POST":
        try:
            question = request.form["question"]
            if DB.get("question"):
                return jsonify({"message": "Question Already exist, please reset."})
            DB["question"] = question
            return jsonify(
                {
                    "message": "Successfully created your question, start sharing the survey."
                }
            )
        except Exception as exc:
            print(str(exc))
            return jsonify({"message": str(exc)})


@app.route("/response", methods=["POST"])
def submit_response():
    if request.method == "POST":
        try:
            check_question_exist()
            yes = request.json["yes"]
            no = request.json["no"]
            DB["answer"]["yes"] += yes
            DB["answer"]["no"] += no
            return jsonify(
                {
                    "message": f"Successfully saved your response for {DB.get('question')}"
                }
            )
        except Exception as exc:
            print(str(exc))
            return jsonify({"message": str(exc)})


@app.route("/survey", methods=["GET"])
def view_survey():
    try:
        check_question_exist()
        return jsonify(DB)
    except Exception as exc:
        print(str(exc))
        return jsonify({"message": str(exc)})


@app.route("/reset", methods=["POST"])
def reset_survey():
    try:
        check_question_exist()
        DB["question"] = ""
        DB["answer"] = {"yes": 0, "no": 0}
        return jsonify(
            {"message": "Your survey has been closed. Please create new one."}
        )
    except Exception as exc:
        print(str(exc))
        return jsonify({"message": str(exc)})


if __name__ == "__main__":
    print("Application starts")
    DB = create_db()
    app.run(debug=True)
