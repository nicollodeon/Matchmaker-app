# Matcher-Maker
CITS3403 Agile Project: A speed dating site purely more matchmaking


Requirements installation: 
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install -r requirements.txt

>>> u = User(username='john', email='john@example.com')
>>> db.session.add(u)
>>> db.session.commit()

>>> users = User.query.all()
>>> for u in users:
...     db.session.delete(u)
...
>>> posts = Post.query.all()
>>> for p in posts:
...     db.session.delete(p)
...
>>> db.session.commit()

for the reverse/delete stuff

db.session.rollback() before commit to roll backu = User(username='susan', email='susan@example.com')


GUIDE:

"venv": virtual environment, a complete copy of python interpreter. Any installed packages go into your venv
"matchmaker.py": call the application
".flaskenv": for flask environmental variables, tells flask that matchmaker.py is the starting point (also turn on debug mode)
"app": A package (any folder is a packages with the init) where the application will be hosted from
- "__init__.py": starts the first Flask object
- "route.py" view function, routes/apply logic to incoming messages
- "forms.py" host the Flask-WTF class that does web forms
- "templates" holds our HTML pages that are routed to from the view function
"config.py" a global configuration file

PROCESS:
 - Start at __init__.py: intialise our objects

Starting the app:
- For the first time, run 'flask db upgrade'
- Please Run 'flask run' to host the application locally

Testing and validation:
- All validation on HTML passes on The W3C Markup Validation Service except the errors got from jinja extension
