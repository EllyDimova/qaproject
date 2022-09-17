from flask import Flask, render_template, request,redirect,url_for, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.secret_key = "Secret key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db =  SQLAlchemy(app)

class Data (db.Model):
    id = db.Column (db.Integer, primary_key = True)
    name = db.Column (db.String(100))
    email = db.Column (db.String(100))
    phone = db.Column (db.String(100))

    def __init__(self,name,email,phone):
        self.name = name
        self.email = email
        self.phone = phone

@app.route('/')
def index():
    all_data = Data.query.all()
    return render_template("index.html", employees=all_data)

@app.route('/insert',methods=['POST'])
def insert():
    if request.method == 'POST':
        name=request.form ['name']
        email=request.form['email']
        phone=request.form['phone']

        my_data = Data(name, email,phone)
        db.session.add(my_data)
        db.session.commit()

        flash ("Employee inserted succsessfully")

    return redirect(url_for('index'))  

   # @app.route('/', methods=['GET','POST'])
#def postName():
    #form = myForm()
    #if form.validate_on_submit():
        #username = form.username.data
        #return render_template('home.html', form = form, username=username)
    #else:
        #return render_template('home.html', form = form, username="") 

@app.route('/update',methods = ['GET', 'POST'])
def update():
    my_data = Data.query.get(request.form.get('id'))
    
    if request.method == 'POST':
        
        print(my_data)
        my_data.name = request.form.get('name')
        my_data.email = request.form.get('email')
        my_data.phone = request.form.get('phone')

        db.session.commit()
        flash("Employee update successfully")
    return redirect(url_for('index'))

@app.route('/delete/<id>', methods = ['GET','POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee deleted successfully")

    return redirect(url_for('index'))

if __name__=="__main__":
    app.run (debug=True, host= '0.0.0.0', port=5000)