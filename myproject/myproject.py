import uuid
import requests
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session  # https://pythonhosted.org/Flask-Session
import script2, ec2, bill, script1, total, total1


app = Flask(__name__,template_folder='templates')

@app.route("/")
def login():
      return render_template('login.html')

@app.route('/index.html', methods = ['POST', 'GET'])
def index1():
    list = ["cz-user"]
    output = request.form.to_dict()
    name = output['name']
    if name in list:
      return render_template('index.html')
    else:
      return render_template('login.html')
      
     
@app.route('/table.html', methods = ['POST', 'GET'])
def myfun():
    output = request.form.to_dict()
    name = output['tvalue']
    reg = output['rvalue']
    ser = output['svalue']
    if ser == 'ec2':
      if name == "Main":
        script1.ec2(name, reg)
        return render_template('table.html')
      else:
        ec2.insta(name, reg)
        return render_template('table.html')

@app.route('/bill.html' , methods = ['POST', 'GET'])
def billing():   
  return render_template('bill.html')
      
@app.route('/billing.html', methods = ['POST', 'GET'])
def bille(): 
    output = request.form.to_dict()
    name = output['tvalue']
    fr = output['from']
    to = output['to']
    if name == "Main":
      script2.fun(name, fr, to)
      return render_template('billing.html')
    else:
      bill.billy(name, fr, to)  
      return render_template('billing.html')

@app.route('/total.html', methods = ['POST', 'GET'])
def bille1():
    output = request.form.to_dict()
    name = output['tvalue']
    fr = output['from']
    to = output['to']
    if name == "Main":
      total.fun(fr, to)
      return render_template('billing1.html')
    else:
      total1.fun(name, fr, to)
      return render_template('billing1.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=33222,debug=True)


