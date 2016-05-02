from flask import Flask
from flask import request
import json

import question_generator as qg

app = Flask(__name__)

@app.route("/article", methods=['GET'])
def hello():
    return "Hello Veha!"

@app.route("/article", methods=['POST'])
def sayHi():
	final_questions = qg.generate_questions(request.form['article'])
	res = {"id": request.form["id"], "quiz": final_questions}
	return json.dumps(res, ensure_ascii=False)

if __name__ == "__main__":
	app.debug = True
	app.run()