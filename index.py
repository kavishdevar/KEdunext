from flask import Flask, request, redirect, url_for, make_response, render_template
import requests
from datetime import datetime, timedelta
tokens = {}

app=Flask(__name__)
baseurl = "localhost:8080"
protocol = "http"

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        next=request.args.get('next')
        resp=make_response(redirect(str(next)))
        resp.set_cookie("username",request.form['username'])
        resp.set_cookie("password",request.form['password'])
        return resp
    else:
        return render_template('login.html')

class Student:
    def __init__(self, username, password,request="all"):
        self.username = username
        self.password = password
        print("logging in with username: "+username+" and password: "+password+"...")
        if request=="all":
            self.update()
        if request=="hw":
            self.hwlist = requests.post(f"{protocol}://{baseurl}/api/v1/homeworks", data={"username": username, "password": password}).json()
        if request=="circular":
            self.circularlist = requests.post(f"{protocol}://{baseurl}/api/v1/circulars", data={"username": username, "password": password}).json()
        self.photoURL = requests.post(f"{protocol}://{baseurl}/api/v1/photo", data={"username": username, "password": password}).text
    def update(self):
        self.hwlist = requests.post(f"{protocol}://{baseurl}/api/v1/homeworks", data={"username": self.username, "password": self.password}).json()
        self.circularlist = requests.post(f"{protocol}://{baseurl}/api/v1/circulars", data={"username": self.username, "password": self.password}).json()
        self.photoURL = requests.post(f"{protocol}://{baseurl}/api/v1/photo", data={"username": self.username, "password": self.password}).text

@app.route('/homeworks')
def homework():
    if request.cookies.get('username')==None:
        return redirect(url_for('login')+f'?next={request.url}')
    user=Student(request.cookies['username'],request.cookies['password'],"hw")
    if "error" in user.hwlist.keys():
        return render_template('homeworks.html',error=user.hwlist["error"],homeworks={},ids=[],photoURL="")
    else:
        return render_template('homeworks.html',homeworks=user.hwlist,ids=sorted(user.hwlist.keys(),reverse=True),photoURL=user.photoURL)

def get_key(dict, val):
   
    for key, value in dict.items():
        if val == value["description"]:
            return key
 
    return "key doesn't exist"

from datetime import datetime

@app.route('/circulars')
def circular():
    if request.cookies.get('username')==None:
        return redirect(url_for('login')+f'?next={request.url}')
    user=Student(request.cookies['username'],request.cookies['password'],"circular")
    if "error" in user.circularlist.keys():
        return render_template('circulars.html',error=user.circularlist["error"],homeworks={},ids=[],photoURL="")
    else:
        # Sort the values based on the date and then the ID
        sorted_dict = dict(sorted(user.circularlist.items(), key=lambda x: datetime.strptime(x[1]['date'], '%d-%m-%Y'), reverse=True))
        return render_template('circulars.html', circulars=sorted_dict, ids=sorted_dict.keys(), photoURL=user.photoURL)

@app.route('/')
def index():
    if request.cookies.get('username')==None:
        return redirect(url_for('login')+f'?next={request.url}')
    user=Student(request.cookies['username'],request.cookies['password'])
    if "error" in user.hwlist.keys():
        return render_template('index.html',error=user.hwlist["error"],homeworks={},ids=[],photoURL="")
    elif  "error" in user.circularlist.keys():
        return render_template('index.html',error=user.circularlist["error"],homeworks={},ids=[],photoURL="")
    else:
        keys=user.circularlist.keys()
        dates=[]
        for key in keys:
            # user.circularlist[key]["date"]=datetime.strptime(user.circularlist[key]["date"], '%d-%m-%Y').date()
            print(user.circularlist[key]["date"])
            dates.append(user.circularlist[key]["date"])
        dates.sort(key = lambda date: datetime.strptime(date, '%d-%m-%Y'), reverse=True)
        ids=[]
        for date in dates:
            for key in keys:
                if user.circularlist[key]["date"]==date:
                    ids.append(key)
                    break
        return render_template('index.html',homeworks=user.hwlist,ids=reversed(sorted(user.hwlist.keys())),photoURL=user.photoURL,circulars=user.circularlist,circularids=ids)

@app.route('/submitHomework/<id>',methods=["POST","GET"])
def submitHomework(id):
    if request.cookies.get('username')==None:
        return redirect(url_for('login'))
    user=Student(request.cookies['username'],request.cookies['password'])
    if request.method=="POST":
        if "error" in user.hwlist.keys():
            return render_template('submitHomework.html',error=user.hwlist["error"],homeworks={},ids=[],photoURL="")
        else:
            submitURL=f'https://dpsgurgaon84.edunext1.com/StudentDashboardApp/submitHomework?homeworkid={id}'
            submit=requests.post(submitURL,data={"username":request.cookies['username'],"password":request.cookies['password'],"file":request.files['file']})
            return submit.text
    else:
        return render_template('submitHomework.html',hw=user.hwlist,photoURL=user.photoURL)


@app.route('/logout')
def logout():
    request.cookies.pop('username')
    request.cookies.pop('password')
    return redirect(url_for('login'))

if __name__=="__main__":
    app.run(host='0.0.0.0',port=8000, debug=True)
