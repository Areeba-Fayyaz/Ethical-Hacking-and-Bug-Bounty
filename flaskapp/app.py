from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import requests

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
        query=f"SELECT user_id, username from users where \
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
            # message=f'Welcome {user}'
            return redirect(url_for('welcome', user_id=user[0]))
        else:
            message=f'Incorrect username or password'
    return render_template('login.html', message = message)

# we will be saving userid as session cookie and will use that session key to do an idor attack 

@app.route('/welcome/<int:user_id>', method=['GET'])
def welcome_page(user_id):
    query=f'select username from users where user_id={user_id}'
    result=db.engine.execute(query)
    user=result.fetchall()

    if user:
        return f'Welcome, {user[0]}! You are logged in.'




bad_chars=["'","#","--",";"]
def black_list(uname):
    for char in bad_chars:
        if char in uname.lower():
            return True
    return False

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Parameterized queries help prevent SQL injection attacks by ensuring that user input is treated as data, not executable code. With placeholders, the database 
    # driver takes care of properly escaping and sanitizing the input, making it much harder for attackers to inject malicious SQL code.
    
    message=''
    if request.method=='POST':
        username = request.form.get('username')
        pswd=request.form.get('pswd')

        if black_list(username):
            message='No Hacking'
            return render_template('register.html',message=message)

        check_query=f"SELECT username from users where \
            username =%s"
        user_exists=db.engine.execute(check_query,(username,)).fetchone()

        if user_exists:
            message='Username already exists!'
        else:
            insert_query='insert into users(username, password) values(%s,%s)'
            db.engine.execute(insert_query,(username,pswd))
            message='Registration Successful!'
            
    return render_template('register.html', message = message)


@app.route('/redirect_page', methods=['GET'])
def redirect_page():
    return render_template('redirect_page.html')

@app.route('/open', methods=['GET'])
def open():
    target_url= request.args.get('url')
    # from the url below line tries to get the value associated with the key action and if action doesn't exist it default to the 'redirect' value
    action=request.args.get('action','redirect')
    
    # open redirection
    # vulnerable part of the code 
   
    if action == 'redirect':
        return redirect(target_url)
    
    # SSRF
    elif action == 'fetch':
        try:
            response = requests.get(target_url, timeout=5)
            if response.status_code==200:
                return f' Received 200 ok {target_url}'
            else:
                return f'Received {response.status_code} from {target_url}'
        except requests.ConnectionError:
            return f'Connection refused by {target_url}'
        except requests.Timeout:
            return f'Connection timed out for {target_url}'
        except Exception as e:
            return str(e)
    return "Specify action and url parameters"
    

# we will be saving userid as session cookie and will use that session key to do an idor attack 



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

