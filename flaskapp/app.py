from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:kali@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db=SQLAlchemy(app)
@app.route('/')
def home():
    return render_template('/index.html') 


@app.route('/about-me', methods=['GET', 'POST'])
def about_me():
    user_input = ''
    if request.method=='POST':
        user_input = request.form.get('name','')

    return render_template('aboutme.html', user_input = user_input)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message=''
    if request.method=='POST':
        username = request.form.get('username')
        pswd=request.form.get('pswd')
        query=f"SELECT username from users where \
            username ='{username}' and password='{pswd}'"
        
        # Input 1: admin'# 
        # when you  put admin'# as input in username, everything after '#' will be commented out so database will only query half
        
        # Input 2: admin'-- 
        # The space after "--" in "admin'-- " is important for proper SQL comment syntax, making the injected comment effective.

        # Input 3: admin' union select password from users;--  
        # to retrieve passwords by combining the original query with a UNION SELECT statement.

        result=db.engine.execute(query)
        user=result.fetchall()

        if user:
            message=f'Welcome {user}'
        else:
            message=f'Incorrect username or password'
    return render_template('login.html', message = message)

#### BASICS ####
# @app.route('/')
# def hello():
#     return 'hello world'

# @app.route('/page<int:number>')
# def page(number):
#     return f'We are on page {number}'

# @app.route('/page<name>')
# def welcome(name):
#     return f'Welcome {name}!'
#### BASICS ####

if __name__=='__main__':
    app.run(debug=True)

