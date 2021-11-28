"""
Asdb Web Status
status.asdb.live
"""
from flask import Flask,request
from flask.templating import render_template

app = Flask(__name__)


@app.route('/')
def Main():
    return "Hello World",200

@app.route('/FixData',methods=['POST','GET'])
def pushFixeData():
    return render_template('FixData.html',postedData=request.form.to_dict())

@app.route('/WorkflowApi',methods=['POST','GET'])
def WorkflowApi():
    if request.args.get('token') == None:
        return 'Token is Required',401