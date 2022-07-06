from http.client import HTTPResponse
import os
import json
from flask import Flask, render_template, request, url_for, redirect, Response
from dotenv import load_dotenv
from .gmail.gmail import send_email
from peewee import *
from playhouse.shortcuts import model_to_dict
import datetime

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            host=os.getenv("MYSQL_HOST"),
            port=3306
    )
print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

#POST method
@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    try:
        name = request.form['name']
        if not name:
            return 'Invalid name', 400
    except KeyError:
        return 'Invalid name', 400
    
    try:
        email = request.form['email']

        if not email or '@' not in email:
            return 'Invalid email', 400
    except KeyError:
        return 'Invalid email', 400

    try:
        content = request.form['content']

        if not content:
            return 'Invalid content', 400
    except KeyError:
        return 'Invalid content', 400
        
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)

#GET method
@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in
                TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }
#GET by id method
@app.route('/api/timeline_post/<id>', methods=['GET'])
def get_time_line_post_id(id):
    p = TimelinePost.get(TimelinePost.id == id)
    return model_to_dict(p)

#DELETE post by id method
@app.route('/api/timeline_post/<id>', methods=['DELETE'])
def delete_time_line_post_id(id):
    p = TimelinePost.get(TimelinePost.id == id)
    p.delete_instance()
    return "Deleted the post with ID=" + id + "\n"

@app.route('/timeline')
def timeline():
        return render_template('timeline.html', title="Timeline")

data = 0
filename = os.path.join(app.static_folder, 'data.json')
with open(filename) as f:
    data = json.load(f)

@app.route("/", defaults={"name": "logan"})
@app.route("/<any(logan, hadi, justin):name>", methods=['GET'])
def index(name):
    anchors = ["Experience", "Education", "Projects", "Trivia", "Hobbies", "Map", "Contact"]
    return render_template('pages/index.html', title=name, url=os.getenv("URL"), data=data, anchors=anchors)

@app.route("/contact", methods=['POST'])
def contact():
    if request.method == 'POST':
        sender_name = request.form.get("name")
        sender_email = request.form.get("email")
        message = request.form.get("message")
        subject = request.form.get("subject")
        receiver_name = request.form.get("receiver_name")
        receiver_email = request.form.get("receiver_email")
        formatted_message = "Name: {}\nEmail: {}\nMessage: {}".format(sender_name, sender_email, message)
        formatted_confirmation = "Hello {},\nYour message for {} has been received.\nThank you.".format(sender_name, receiver_name)
        send_email(receiver_name, receiver_email, subject, formatted_message)
        send_email(sender_name, sender_email, "Email Confirmation", formatted_confirmation)
        return '', 204


@app.errorhandler(404)
def page_not_found(e):
    # Set the 404 status explicitly
    return render_template('pages/404.html'), 404
