from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Create the application context
with app.app_context():
    db = SQLAlchemy(app)
    # Perform database operations within the application context
    # creating a class for database table
    # define the table,columns, attributes used in database table.
    # see the Capital letter iotherwise got errors
    # remeber the MVC architecture

    class TODO(db.Model):
        sno = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(200), nullable=False)
        desc = db.Column(db.String(500), nullable=False)
        date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # used to what i want to see when i add something in database
    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"
    db.create_all()

# app.route are the endpoints that means where to go
# make action="/" in html file to get and post data


@app.route("/", methods=['GET', 'POST'])
# now what i want when someone come to the home page, a todo instance shoulld be created and added to the database
def create():
    if request.method == 'POST':
        # here you have to use the (name) of the input field ['title'] coming from html file
        title = request.form['title']
        # here you have to use the (name) of the input field ['desc'] coming from html file
        description = request.form['desc']
        # now after getting data store in variables, now we have to store data in data base. creating instance of TODO class.
        todo = TODO(title=title, desc=description)
        db.session.add(todo)  # adding data to database
        db.session.commit()  # commiting data to database

    # here after the data is added to database, now we have to show the data to the user here at the same time.
    # query to extract all data from table
    todo = TODO.query.all()
    return render_template("index.html", todos=todo)


@app.route("/show")
# now what i want when someone come to the home page, a todo instance shoulld be created and added to the database
def show():
    todo = TODO.query.all()
    return render_template("index.html", todos=todo)


@app.route("/delete/<int:sno>")  # know theformat to avoid errors
# now what i want when someone come to the home page, a todo instance shoulld be created and added to the database
def delete(sno):
    # filter by sno and get the first one
    todo = TODO.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")  # after deleting it will redirect to home page

# @app.route("/update")
# # now what i want when someone come to the home page, a todo instance shoulld be created and added to the database
# def update():
#     todo = TODO(title="First todo", desc="This is my first todo")
#     db.session.add(todo)
#     db.session.commit()
#     return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
