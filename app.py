from functools import reduce
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime




app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///subh.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Subh(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title= db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods = ["GET", "POST"])
def hello_world():
    if request.method == "POST":
         title = request.form["title"]
         desc = request.form["desc"]
    
         todo = Subh(title=title, desc=desc )
         db.session.add(todo)
         db.session.commit()



    allTodo = Subh.query.all()
    return render_template("index.html", allTodo=allTodo)
     
    
    
   
       


@app.route('/Home')
def Home():
    allTodo = Subh.query.all()
    print(allTodo)
    return "<h1>Welcome to home page</h1>"

@app.route('/update/<int:sno>' , methods = ["GET", "POST"])
def upadte(sno):
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        AllTodo = Subh.query.filter_by(sno=sno).first()
        AllTodo.title = title
        AllTodo.desc = desc 
        db.session.add(AllTodo)
        db.session.commit()
        return redirect('/')

    todo = Subh.query.filter_by(sno=sno).first()
    return render_template("update.html", AllTodo=todo)

    


@app.route('/delete/<int:sno>')
def delete(sno):
   allTodo = Subh.query.filter_by(sno=sno).first()
   db.session.delete(allTodo)
   db.session.commit()
   return redirect('/')




if __name__ == "__main__":
    app.run(debug=True)   # i can also add host and port.

