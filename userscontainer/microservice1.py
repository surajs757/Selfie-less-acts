import sys
import base64
from flask import Flask, render_template, request, redirect, Response , abort, jsonify, make_response, Response
import random, json
from json import dumps
import base64
import binascii
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

total_reqs=0

@app.route('api/v1/_count',methods=['GET'])
def get_reqs():
    if(request.method!= "GET"):
        abort(405)
    
    global total_reqs
    return jsonify([total_reqs]),200


@app.route('api/v1/_count',methods=['DELETE'])
def reset_count():
    if(request.method!= "DELETE"):
        abort(405)

    global total_reqs
    total_reqs=0


@app.route('/api/v1/users', methods=['POST'])
def chk_credentials():
    global total_reqs
    total_reqs+=1
    if(request.method != "POST"):
        abort(405)    
    """
    if(request.is_json):
        return "yes"
    else:
        return "no"
    """
    #return "hello there"
    data= request.get_json(force=True)
    
    user=""
    password=""
    
    user+=(str(data['username']))
    password+=(str(data['password']))
    #return user
    
    f=open("static/usernames.txt","r")
    existusers=[x.split('\t')[0] for x in f.readlines()]
    for name in existusers:
        if(user==name):
            abort(400)
        
    if(len(password)!=40):
        abort(400)
    
    for char in password:
        
        if ((((char>='0' and char<='9') or (char>='A' and char<='F') or (char>='a' and char<='f'))) != True):
            #return password
            abort(400)

    f.close()
    
    st=user+"\t"+password+"\n"
    f=open("static/usernames.txt","r")
    existing_users=f.readlines()
    existing_users.append(st)
    f.close()
    f=open("static/usernames.txt","w")
    f.write("".join(existing_users))
    f.close()
    return "user added successfully", 201
    

@app.route('/api/v1/users/<username>',methods=['DELETE'])
def rem_user(username):
    global total_reqs
    total_reqs+=1
    if(request.method != "DELETE"):
        abort(405)    
    f=open("static/usernames.txt","r")        
    creds=f.readlines()
    #return creds[0]
    names=[x.split('\t')[0] for x in creds]
    #return str(len(names))
    #return username
    if username not in names:
        abort(400)
    else:
        reqcred=""
        for cred in creds:
            if(username==cred.split()[0]):
                reqcred=cred
                break
        creds.remove(reqcred)
        st=''.join(creds)
        #return st
        f.close()
        f=open("static/usernames.txt","w")
        f.write(st)
        
    st="user "+username+" removed successfullly"
    return str(st),200


@app.route('/api/v1/users',methods=['GET'])
def list_users():
    global total_reqs
    total_reqs+=1
    if(request.method != "GET"):
        abort(405)    
    f=open("static/usernames.txt","r")
    creds=f.readlines()
    names=[x.split('\t')[0] for x in creds]
    if (len(names)==0):
        return "No users",204

    return jsonify(names)




if __name__ == "__main__":
    app.debug=True
    app.run(host="0.0.0.0",port=8000)
    #app.run(port=4000)
