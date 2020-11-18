from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.secret_key = "secretkey"
app.config["SECRET_KEY"] = "SECRET"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)


@app.route("/home")
@app.route("/")
def index():
    """Renders title and info, then redirects to session after survey selection"""

    title = "Survey Selection"
    info = "Choose a survey that you'd like to take!"
    surveys_lst = surveys.surveys

    return render_template("home.html", title=title, info=info, surveys=surveys_lst)


@app.route("/session", methods=["POST"])
def session_start():
    """Begins session["responses"] and initializes question input"""

    session["responses"] = []
    session["chosen_title"] = request.form.get("survey_choice", "satisfaction")
    print(session["chosen_title"])

    responses_length = len(session["responses"])
    return redirect(f"/question/{responses_length}")


@app.route("/question/<int:id>")
def question(id):
    """Renders each question per the selected survey depending on
    the ID (length of session["responses"]"""

    responses_length = len(session["responses"])
    print(surveys.surveys["satisfaction"].questions)

    # stops user from gaining access to other questions of different surveys
    if id >= len(surveys.surveys[session["chosen_title"]].questions):
        return redirect("/end")

    # handle invalid id on /question/(bad id)
    if id != responses_length:
        return redirect(f"/question/{responses_length}")

    question = surveys.surveys[session["chosen_title"]].questions[id].question
    choices = surveys.surveys[session["chosen_title"]].questions[id].choices

    return render_template("question.html", question=question, choices=choices)


@app.route("/answer", methods=["POST"])
def answer():
    """Save answers in the session res and redirect to the next question"""

    answer = request.form
    sess = session["responses"]
    sess.append(answer["choice"])
    session["responses"] = sess
    id = len(session["responses"])

    return redirect(f"/question/{id}")


@app.route("/end")
def end():
    """Ending page"""

    return render_template("end.html")