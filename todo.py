from flask import Flask,render_template,request,redirect,url_for,jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rishabhgajra@localhost:5432/fsdegree'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    __tablename__='todosnew'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(),nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

db.create_all() #creating all tables

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())


@app.route('/todo/create',methods=['POST'])
def create():
    print("oye")
    desc=request.get_json()['description']
    todo=Todo(description=desc)
    db.session.add(todo)
    db.session.commit()
    return jsonify({
        'description':todo.description
    })
