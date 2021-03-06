from flask import Flask, request, redirect, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy #載入資料庫連線擴充套件
from datetime import datetime
db = SQLAlchemy()
app=Flask(
    __name__,
    static_url_path="/"
) #建立app物件
app.config['SECRET_KEY'] = 'becky' #用來解決flask使用session產生的錯誤

#MySQL Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:becky1qaz2wsx@localhost:3306/website"
# 模型( model )定義
#--------------------database---------------
# 獲取SQLAlchemy例項物件
db = SQLAlchemy()
db.init_app(app)
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
#-----------------------------------------------        


#建立路徑/對應的處理函式
@app.route("/")
def index(): #用來回應網站首頁連線的函式
    return render_template("index.html")

@app.route("/member")
def member():
    if session["user_status"] == "signin":
        return render_template("member.html")
    else:
        return redirect("/")


@app.route("/error", methods=["GET"])
def error(): 
    errorMessage=request.args.get("message","")
    return render_template("error.html",errorMessage=errorMessage)

@app.route("/signup", methods=["POST"])
def signup():
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    username_check = User.query.filter_by(username=username).first()
    if username_check:
        return redirect(url_for('error',message='帳號已被註冊'))
    else:
        create_user = User(name=name,username=username,password=password)
        db.session.add(create_user)
        db.session.commit()
        return redirect('/member')    

 


@app.route("/signin", methods=["POST"]) #不寫的話其實預設就是GET
def signin(): 
    username=request.form["username"]
    password=request.form["password"]
    check_username_and_password = User.query.filter_by(username=username,password=password).first()
    if check_username_and_password:
        name = check_username_and_password.name
        session['username'] = username
        session["user_status"]="signin"
        return render_template("member.html",name=name)
    else:
        return redirect(url_for("error",message='帳號或密碼輸入錯誤'))

@app.route("/signout", methods=["GET"]) 
def signout(): 
    session["user_status"]="signout"
    return redirect("/")



app.run(port=3000) #啟動網站伺服器
