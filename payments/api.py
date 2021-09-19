import flask
import os as os
import requests
import hashlib
from flask import url_for
from flask import render_template, make_response
from model.filetransaction import transcation
import json
from flask import Flask, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True


t = transcation()

t.random_string(7,5)
t.genrateReceiptNo()


@app.route('/', methods=['GET'])
def home():
    cost = request.args.get('cost')

    if(cost==None):
       print("hi")
       return render_template("error.html")


    value = {
        'key': t.getmerchantKey(),
        'txnid': t.getTXNid(),
        'productinfo': 'Ride',
        'amount': str(cost),
        'email':'ankita9shreya@gmail.com',
        'firstname': 'PayU',
        'surl': 'http://192.168.29.186:8080/checkstatus',
        'furl': 'http://192.168.29.186:8080/checkstatus',
        'phone': '9876543210',
        'hash': 'hehfhh',
        'receiptNo': t.getreceiptNo()
     }

    strliteral = value['key']+"|"+value['txnid']+"|"+value['amount']+"|"+value['productinfo']+"|"+value['firstname']+"|"+value['email']+"|||||||||||"+t.getSALT()
    hashvalue = hashlib.sha512(strliteral.encode())
    value['hash'] = hashvalue.hexdigest()

    render_template("index.html",data = value)

    # resp = {
    #     "status": "Inprogress"
    # }

    return render_template("index.html",data = value)


@app.route('/checkstatus', methods=['POST'])
def checkstatuslf():
    return render_template("status.html")


@app.route('/transactionInfo', methods=['GET'])
def transacdetails():

    url = "https://test.payu.in/merchant/postservice?form=2"
    strliteral = t.getmerchantKey()+'|verify_payment|'+t.getTXNid()+'|'+t.getSALT()
    strliteralHex= hashlib.sha512(strliteral.encode()) 
    hashvalue = strliteralHex.hexdigest()
    payload = 'key='+t.getmerchantKey()+'&command=verify_payment&var1='+t.getTXNid()+'&hash='+hashvalue
    headers = { "Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded" }

    r = requests.request("POST", url, data=payload, headers=headers)

    f = r.json()

    if(f['status']==0):
       return render_template("success.html")
    else:
       return render_template("failure.html")
    
    

if __name__=="__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 8080)))

