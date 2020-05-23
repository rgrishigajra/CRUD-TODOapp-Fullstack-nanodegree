from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rishabhgajra@localhost:5432/fsdegree'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todosnew'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.String(), nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey(
        "todolists.id"), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


class TodoList(db.Model):
    __tablename__ = "todolists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref="todolist", lazy=True)
# db.create_all()  # creating all tables


@app.route('/')
def index():
    return redirect(url_for('lists', list_id=1))


@app.route('/lists/<list_id>')
def lists(list_id):
     
     return render_template('index.html',todos=Todo.query.filter_by(list_id=list_id).order_by("id").all(),
     active_list=TodoList.query.get(list_id),
     todolists=TodoList.query.all())



@app.route('/todo/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)


@app.route("/todo/<todo_id>/check", methods=['POST'])
def check_box(todo_id):
    print(request.get_json()['checked'], todo_id)
    body = {}
    try:
        checked = request.get_json()['checked']
        checking = Todo.query.get(todo_id)
        checking.completed = checked
        print(checking.query.all())
        db.session.commit()
        body['checked'] = checked
        body['id'] = todo_id
    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    return jsonify(body)


@app.route("/todo/<todo_id>/delete", methods=["GET"])
def delete(todo_id):
    print(todo_id)
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info)
    finally:
        db.session.close()
    return "ok"
