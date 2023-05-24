from flask import Flask, request, redirect, url_for, make_response, render_template
import pydunext
import requests

app=Flask(__name__)

baseurl = "kedunext.azurewebsites.net"
protocol = "https"

import time

class User:
    def __init__(self, username, password,request="all"):
        self.username = username
        self.password = password
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

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        resp=make_response(redirect(url_for('index')))
        resp.set_cookie("username",request.form['username'])
        resp.set_cookie("password",request.form['password'])
        return resp
    else:
        return render_template('login.html')

@app.route('/homeworks')
def homework():
    if request.cookies.get('username')==None:
        return redirect(url_for('login'))
    user=User(request.cookies['username'],request.cookies['password'],"hw")
    if "error" in user.hwlist.keys():
        return render_template('homeworks.html',error=user.hwlist["error"],homeworks={},ids=[],photoURL="")
    else:
        return render_template('homeworks.html',homeworks=user.hwlist,ids=sorted(user.hwlist.keys(),reverse=True),photoURL=user.photoURL)
from datetime import datetime
@app.route('/circulars')
def circular():
    if request.cookies.get('username')==None:
        return redirect(url_for('login'))
    user=User(request.cookies['username'],request.cookies['password'],"circular")
    if "error" in user.circularlist.keys():
        return render_template('circulars.html',error=user.circularlist["error"],homeworks={},ids=[],photoURL="")
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
        return render_template('circulars.html',circulars=user.circularlist,ids=ids,photoURL=user.photoURL)

@app.route('/')
def index():
    if request.cookies.get('username')==None:
        return redirect(url_for('login'))
    user=User(request.cookies['username'],request.cookies['password'])
    if "error" in user.hwlist.keys() or "error" in user.circularlist.keys():
        return render_template('index.html',error=user.hwlist["error"],homeworks={},ids=[],photoURL="")
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
    
if __name__=="__main__":
    app.run(host='0.0.0.0',port=8000, debug=True)
