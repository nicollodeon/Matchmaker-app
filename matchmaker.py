from app import app, db                             # from directory app, import the variable app
from app.models import User, Post

@app.shell_context_processor                        # for running flask shell (set up enviroment var) so don't need to import every time
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}