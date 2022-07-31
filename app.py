import email
import re
from flask import Flask, render_template,request,flash,url_for,redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import ForeignKey


    
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///airport.db"
app.secret_key = 'kunji andrew'
db = SQLAlchemy(app)


class city(db.Model):
    id = db.Column('city_id' , db.Integer , primary_key = True)
    name = db.Column('city_name' , db.String(50))

    def __init__(self ,name):
        self.name = name

# class airport(db.Model):
#     id = db.Column('airport_id' , db.Integer , primary_key = True)
#     name = db.Column('airport_name' , db.String(50))          
#     city = db.Column('city_id' , db.Integer)

#     def __init__(self , name , city):
#         self.name = name
#         self.city = city

class flights(db.Model):        
    id = db.Column('flight_id' , db.Integer , primary_key = True)
    num = db.Column('flight_number' , db.Integer)
    name = db.Column('flight_name' , db.String(50))          
    # a_id = db.Column('airport_id' , db.Integer)
    r_id = db.Column('route_id' , db.Integer , ForeignKey("routes.route_id") )
    date = db.Column('date' , db.DateTime)

    def __init__(self , name , num , r_id,date):
        self.name = name
        # self.a_id = a_id
        self.num = num
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
                 return redirect(url_for('addcity')) 
            else:    
                return redirect(url_for('search')) 
    else:
        return redirect(url_for('home'))        

       

@app.route('/login', methods=['GET','POST'])
def login():
    if(request.method == 'POST'):
        if not request.form['name'] or not request.form['password']:
            flash('Please enter all the fields', 'error')
        else:
            data = user.query.filter_by(name = request.form['name']).first()
            if(data):
                print('succes',data.p_e)
                session['username']=request.form['name']
                session['type']=data.p_e
                # data= user.query.filter_by(name = request.form['name']).all()
                print(data.p_e)
                if data.p_e == 'e':
                    return redirect(url_for('addcity')) 
                else:
                    return redirect(url_for('search')) 
            else:
                print('failed')
                # flash('Record was successfully added')
                return redirect(url_for('login'))
    return render_template('/login.html')


@app.route("/search" , methods = ['GET','POST'] )
def search():
    data = routes.query.all()
    result = db.session.query(flights , routes).outerjoin(flights , flights.r_id == routes.id)
    if request.method == 'GET':
        for i in data:
            print(i)
        print("called")
        return render_template('search.html', data=data , result = result)   

    elif request.method == 'POST':
        rid = request.form['rid']
        result = db.session.query(flights , routes).outerjoin(flights , flights.r_id == rid)
        render_template('search.html' , data = data , reuslt = result)


@app.route('/addcity' , methods = ['GET' , 'POST'])
def addcity():
    if request.method == 'POST':
        name = request.form['name']
        data = city(name)
        db.session.add(data)
        db.session.commit()
    data = city.query.all()
    return render_template('addcity.html', data = data)    

@app.route('/addroute' , methods = ['GET' , 'POST'])
def addroute():
    if request.method == "POST":
        From = request.form['from']
        to = request.form['to']
        price = request.form['price']
        data = routes(From , to , price)
        db.session.add(data)
        db.session.commit()
    data = routes.query.all()
    cities = city.query.all()
    for i in data:
        print(i.From)
    return render_template('addroute.html', data= data, cities=cities)    


@app.route('/addflight' , methods = ['GET' , 'POST'])
def addflight():
    if request.method == 'POST':
        num = request.form['num']
        name = request.form['name']
        rid = request.form['rid']
        date = request.form['date']
        date_time_obj = datetime.strptime(date,'%Y-%m-%dT%H:%M')
        data = flights(name , num , rid ,date_time_obj)
        db.session.add(data)
        db.session.commit()
    data = routes.query.all()
    flights_data = flights.query.all()
    for flight in flights_data:
        route_doc = routes.query.filter_by(id=flight.r_id).first()
        flight.rid=route_doc
    return render_template('addflight.html', data=data, flights=flights_data)    

@app.route('/viewFlights' , methods = ['GET' , 'POST'])
def viewFlights():
    if request.method == 'GET' and session['type'] != 'e':
        return render_template('p4.html')


if __name__ == "__main__":
    db.create_all()
    app.run(host = '0.0.0.0' , debug = True)         
    