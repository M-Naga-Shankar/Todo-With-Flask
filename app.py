from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

#database creation
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    desc = db.Column(db.String)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"

#routes Creations

@app.route('/' , methods=['GET','POST'])
def hello_world():
    status=0
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    if request.method=="GET":
        status=request.args.get('status')

    alltodos=Todo.query.all() 
    print (status)
    return render_template('index.html',alltodo=alltodos,status=status)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/?status=1")

@app.route("/update/<int:sno>", methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/?status=2")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)
#main testing
if __name__== '__main__':
    app.run(debug='True',port=8000)
    
