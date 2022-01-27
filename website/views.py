from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
#from website.auth import login

#has a bunch of URLs defined in it
views = Blueprint('views', __name__)

#This function will run whenever we run the slash route (/)
#whatever is inside the function will run
#Added POST methods to make sure it is allowed for this route 
@views.route('/', methods=['GET', 'POST']) #<-- this is called a decorator
@login_required #This decorator makes sure that you cannot get to the home page unless you are logged in
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    #user=current_user means that, in our template, we will be able to reference this current user and check if it's authenticated
    return render_template("home.html", user=current_user) 

@views.route('/delete-note', methods=['POST'])
def delete_note():
    #This takes in data from the POST request. It will load it as a json object or a python dictionary
    note = json.loads(request.data)
    noteId = note['noteId'] # We then access the noteId attribute
    note = Note.query.get(noteId) #Look for the note that has that ID
    if note: #Check if it exists
        #If the user that is signed in actually owns this note, they can delete it
        if note.user_id == current_user.id: 
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({}) #returning an empty response