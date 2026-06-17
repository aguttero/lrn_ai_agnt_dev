# TO AVOID SHARING THE SAME SESSION AMONG USERS:
import uuid

from flask import Flask, redirect, request, session, url_for
from flask.templating import render_template

from sec5_sqlite import agent, get_location

app = Flask(__name__)
app.secret_key = "choose_secret_key"


@app.route("/")
def home():
    session["thread_id"] = str(uuid.uuid4())
    if "messages" not in session:
        session["mesages"] = []
    print("home:", session)
    # test_list = ["ai", "human"]
    return render_template("chat.html", messages=session["messages"])


@app.route("/send", methods=["POST"])
def send():
    user_message = request.form["message"]
    # user_message = request.form
    user_lat = request.form.get("latitude")
    user_lon = request.form.get("longitude")
    print(f"user_lat= {user_lat} user_lon= {user_lon}")

    print(f"user_message= {user_message} /send route")
    # agent_prompt = {"messages": [{"role": "user", "content": user_message}]}
    # response = agent.invoke(agent_prompt, {"configurable": {"thread_id": "1"}})
    # response = agent.invoke(agent_prompt, {"configurable": {"thread_id": session['thread_id']}})
    # print(f"response=\n{response}")
    # session["messages"] = []
    session["messages"].append({"type": "human", "content": user_message})
    session["messages"].append({"type": "ai", "content": "respuesta_ai"})
    session.modified = True
    print(f"session= \n{session}")
    return redirect(url_for("home"))


@app.route("/another")
def another():
    return f"Hello this is the {another.__name__} page "


get_location()
app.run(port=5001, debug=True)
