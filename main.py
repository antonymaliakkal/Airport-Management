import email
import re
from flask import Flask, render_template,request,flash,url_for,redirect,session
from flask_sqlalchemy import SQLAlchemy


    
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///airport.db"
app.secret_key = 'kunji andrew'
db = SQLAlchemy(app)


class city(db.Model):
    id = db.Column('city_id' , db.Integer , primary_key = True)
    name = db.Column('city_name' , db.String(50))

    def __init__(self ,name):
        self.name = name

class airport(db.Model):
    id = db.Column('airport_id' , db.Integer , primary_key = True)
    name = db.Column('airport_name' , db.String(50))          
    city = db.Column('city_id' , db.Integer)

    def __init__(self , name , city):
        self.name = name
        self.city = city

class flights(db.Model):        
    id = db.Column('flight_id' , db.Integer , primary_key = True)
    name = db.Column('airport_name' , db.String(50))          
    a_id = db.Column('airport_id' , db.Integer)
    r_id = db.Column('route_id' , db.Integer)
    date = db.Column('date' , db.TIMESTAMP)

    def __init__(self , name , a_id , r_id,date):
        self.name = name
        self.a_id = a_id
        self.r_id = r_id
        self.date = date

class routes(db.Model):
    id = db.Column('route_id' , db.Integer , primary_key = True)
    From = db.Column('from' , db.Integer)
    to = db.Column('to' , db.Integer)
    price = db.Column('price' , db.Integer)

    def __init__(self , From , to , price):
        self.From = From
        self.to = to
        self.price = price
        
class tickets(db.Model):
    id = db.Column('ticket_id' , db.Integer , primary_key = True)
    r_id = db.Column('route_id' , db.Integer)
    p_id = db.Column('passenger_id' , db.Integer)
    price = db.Column('total_price' , db.Integer)
    n = db.Column('Number of People' , db.Integer)

    def __init__(self , r_id , p_id , price , n):
        self.r_id = r_id
        self.p_id = p_id
        self.price = price
        self.n = n

class user(db.Model):
    id = db.Column('user_id' , db.Integer , primary_key = True)
    name = db.Column('name' , db.String(100))
    email = db.Column('email' , db.String(100))
    password = db.Column('password' , db.String(100))
    p_e = db.Column('Pasenger/Employee' , db.String(10))

    def __init__(self , name , email , password , p_e): 
        self.name = name 
        self.email = email
        self.password = password
        self.p_e = p_e

@app.route('/')
def home():
    # if(session.get('username')):
    #     re
    # else:    
        return render_template("/login.html")

@app.route('/signup' , methods = ['GET' , 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'] 
        if not(name or email or password):
            flash('Enter all fields' , 'error')
        else:       
            if(request.form['pe'] == 'Employee'):
                pe = 'e'
            else:
                pe = 'p'
            data = user(name , email , password , pe)
            db.session.add(data)
            db.session.commit()
            print('Registered')
            # flash('Registered')
            if pe == 'e':
                 #return redirect(url_for('addcity'))
                 return render_template("addcity.html") 
            else:    
                return render_template("search.html")
    else:
        return redirect(url_for('home'))        

       

@app.route('/login', methods=['GET','POST'])
def login():
    if(request.method == 'POST'):
        if not request.form['name'] or not request.form['password']:
            flash('Please enter all the fields', 'error')
        else:
            data = user.query.filter_by(name = request.form['name']).all()
            if(len(data))>0:
                print('succes')
                session['username']=request.form['name']
                # data= user.query.filter_by(name = request.form['name']).all()
                return redirect(url_for('search')) 
            else:
                print('failed')
                # flash('Record was successfully added')
                return redirect(url_for('login'))
    return render_template('/login.html')


    
# def search():
#     # data = city.query.with_entities(city.city_name)
#     data = city.query.filter_by(name='Ernakulam').first()
#     print(data)
#     for i in data:
#         print(i)
#     if request.method == 'POST':
#         return render_template("search.html" , data = data)


@app.route("/search" , methods = ['GET','POST'] )
def search():
    if request.method == 'GET':
        data = city.query.filter_by(name='Ernakulam')
        print(data)
        for i in data:
            print(i)
        return render_template("search.html" , data = data)
        # return render_template("/search.html")

@app.route('/addcity' , methods = ['GET' , 'POST'])
def addcity():
    if request.method == 'POST':
        name = request.form['name']
        data = city(name)
        db.session.add(data)
        db.session.commit()
        return render_template('addcity.html')


if __name__ == "__main__":
    db.create_all()
    app.run(host = '0.0.0.0' , debug = True)         