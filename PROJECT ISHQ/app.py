from flask import Flask,request 
from twilio.twiml.messaging_response import MessagingResponse
import json 
app = Flask(__name__)
@app.route('/',methods=['GET','POST'])
def index():
    return "hello world"
@app.route('/sms',methods=['GET','POST'])
def response():
    stuff = request.form 
    print(stuff)
    return 'kk'
if __name__ == '__main__':
    app.run(port='5001')
