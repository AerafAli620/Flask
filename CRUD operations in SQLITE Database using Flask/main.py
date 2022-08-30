from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
# Creating database file in currect directory
db_path=os.path.join(os.path.dirname(__file__))
uri='sqlite:///'+os.path.join(db_path,'dbfile.sqlite')
app = Flask(__name__)
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI']=uri
db=SQLAlchemy(app)
# Creating Table (User) 
class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30))
    email=db.Column(db.String(30))
    phone=db.Column(db.String(30))
db.create_all()
# Default route
@app.route('/')
def func():
    return render_template('index.html')

# Creating route for uploading data into the database.
@app.route('/upload_data',methods=['GET','POST'])
def upload_data():
    if request.method=='POST':
        name=request.form.get('username')
        email=request.form.get('useremail')
        phone=request.form.get('userphone')
        entry=User(name=name, email=email, phone=phone)
        db.session.add(entry)
        db.session.commit()
    return render_template('index.html')
# Creating route for showing database all data.
@app.route("/view")
def view():
    users=User.query.all()
    return render_template("viewData.html",users=users)
# Creating route for updating table
@app.route("/update_data",methods=['GET','POST'])
def Update():
    if request.method=='POST':
        userid=request.form.get('target_id')
        username=request.form.get('target_name')
        userphone=request.form.get('target_phone')
        useremail=request.form.get('target_email')
        userfound=User.query.filter_by(id=userid).first()
        userfound.name=username
        userfound.email=useremail
        userfound.phone=userphone
        db.session.add(userfound)
        db.session.commit()
        users=User.query.all()
        return render_template('viewData.html', users=users)
# Creating route for deleting any record
@app.route('/delete',methods=['GET','POST'])
def delete():
    if request.method=='POST':
        targetuser=request.form.get('deleteditem')
        userfound=User.query.filter_by(id=targetuser).first()
        db.session.delete(userfound)
        db.session.commit()
    users=User.query.all()
    return render_template('viewData.html',users=users)

if __name__=='__main__':
    app.run(debug=True)
