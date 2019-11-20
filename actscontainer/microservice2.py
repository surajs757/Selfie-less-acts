import requests
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
acts_uploaded=0

crash=0

@app.route('/api/v1/_health', methods=['GET'])     #
def health_check():
    global crash
    if(crash!=0):
        abort(500)
    if(request.method!= "GET"):
        abort(405)
    #return "",500
    r=requests.get('http://127.0.0.1:5000/api/v1/_count')
    if(r.status_code == 500):
        
        abort(500)
    r=requests.delete('http://127.0.0.1:5000/api/v1/_count')
    if(r.status_code == 500):
        abort(500)
    r=requests.get('http://127.0.0.1:5000/api/v1/acts/count')
    if(r.status_code == 500):
        abort(500)
    r=requests.get('http://127.0.0.1:5000/api/v1/categories')
    if(r.status_code == 500):
        abort(500)
    r=requests.post('http://127.0.0.1:5000/api/v1/categories')
    if(r.status_code == 500):
        #return "no json passed",200
        abort(500)
    r=requests.delete('http://127.0.0.1:5000/api/v1/categories/categoryName')
    if(r.status_code == 500):
        abort(500)
    r=requests.get('http://127.0.0.1:5000/api/v1/categories/categoryName/acts/size')
    if(r.status_code == 500):
        abort(500)
    r=requests.get('http://127.0.0.1:5000/api/v1/categories/categoryName/acts')
    if(r.status_code == 500):
        abort(500)
    r=requests.post('http://127.0.0.1:5000/api/v1/acts/upvote')
    if(r.status_code == 500):
        #return "no json passed",200
        abort(500)
    r=requests.delete('http://127.0.0.1:5000/api/v1/acts/<actId>')
    if(r.status_code == 500):
        abort(500)
    r=requests.post('http://127.0.0.1:5000/api/v1/acts')
    if(r.status_code == 500):
        #return "no json sent",200
        
        abort(500)

    return "server functioning normally",200


@app.route('/api/v1/_crash',methods=['POST'])
def crash_server():
    if(request.method!= "POST"):
        abort(405)

    global crash
    crash=1
    return 200

@app.route('/api/v1/_count',methods=['GET'])        #
def get_reqs():
    global crash
    if(crash!=0):
        abort(500)
    if(request.method!= "GET"):
        abort(405)
    
    global total_reqs
    return jsonify([total_reqs]),200


@app.route('/api/v1/_count',methods=['DELETE'])       #
def reset_count():
    global crash
    if(crash!=0):
        abort(500)
    if(request.method!= "DELETE"):
        abort(405)

    global total_reqs
    total_reqs=0
    return "reset",200

@app.route('/api/v1/acts/count',methods=["GET"])  #
def get_no_acts():
    global crash
    if(crash!=0):
        abort(500)
    if(request.method!= "GET"):
        abort(405)

    global acts_uploaded
    return jsonify([acts_uploaded]),200



@app.route('/api/v1/categories',methods=['GET'])   #
def list_cate():
    global crash
    if(crash!=0):
        abort(500)
    global total_reqs
    total_reqs+=1
    if(request.method != "GET"):
        abort(415)
    #return "hel;lo"
    dic={}
    f=open("static/categories.txt","r")
    dic={}
    arr=f.readlines()
    if(len(arr)==0):
        return "no categories",204
    for line in arr:
        dic[line.split('\t')[0]]=int(line.split('\t')[1])

    
    return jsonify(dic)
    

@app.route('/api/v1/categories',methods=['POST'])       #
def add_cate():
    global crash
    if(crash!=0):
        abort(500)
    global total_reqs
    total_reqs+=1
    if(request.method != "POST"):
        abort(415)
    data= request.get_json(force=True)
    
   
    
   
    to_be_added=str(data[0])
    #return to_be_added
    f=open("static/categories.txt","r")
    categories=f.readlines()
    categorie_names=[x.split('\t')[0] for x in categories]
    if(to_be_added in categorie_names):
        abort(400)
    else:
        st=str(to_be_added)+"\t"+"0\n"
        categories.append(st)
        f.close()
        f=open("static/categories.txt","w")
        f.write("".join(categories))
    return "added successfully",201


@app.route('/api/v1/categories/<categoryName>',methods=['DELETE'])      # 
def del_cate(categoryName):
    global crash
    if(crash!=0):
        abort(500)
    global total_reqs
    total_reqs+=1
    if(request.method != "DELETE"):
        abort(415)
    f=open("static/categories.txt","r")
    categories=f.readlines()
    categorie_names=[x.split('\t')[0] for x in categories]
    if(categoryName not in categorie_names):
        abort(400)
    else:
        reqcate=""
        for category in categories:
            if(categoryName==category.split()[0]):
                reqcate=category
                break
        categories.remove(reqcate)
        st=''.join(categories)
        #return st
        f.close()
        f=open("static/categories.txt","w")
        f.write(st)
        f.close()
        f=open("static/acts_info.txt","r")
        acts=f.readlines()
        tbd_acts=[]
        for act in acts:
            if(act.split('\t')[1]==categoryName):
                tbd_acts.append(act)

        for act in tbd_acts:
            acts.remove(act)
        
        new_acts="".join(acts)
        f.close()
        f=open("static/acts_info.txt","w")
        f.write(new_acts)
        f.close()

    st="category "+categoryName+" removed successfullly"
    return str(st),200


"""    
@app.route('/api/v1/categories/<categoryName>/acts',methods=['GET'])
def list_acts(categoryName):
    f=open("static/categories.txt","r")
    categories=f.readlines()
    categorie_names=[x.split('\t')[0] for x in categories]
    if(categoryName not in categorie_names):
        abort(400)
    f.close()
    f=open("static/acts_info.txt","r")
    acts=f.readlines()
    dic=[]
    cnt=0
    for act in acts:
        newd={}
        if(act.split('\t')[1]==categoryName):
            cnt+=1
            if(cnt>100):
                abort(413)
            newd["actId"]=act.split('\t')[0]
            #return act.split('\t')[4]
            newd["username"]=act.split('\t')[3]
            newd["timestamp"]=act.split('\t')[5]
            newd["caption"]=act.split('\t')[2]
            newd["upvotes"]=act.split('\t')[6]
            
            imgn=act.split('\t')[7][:-1]
            image = open("static/"+imgn, 'rb')
            image_read = image.read()
            image_64_encode = base64.encodestring(image_read)
            #return image_64_encode
            
            newd["imgB64"]=act.split('\t')[7][:-1]
            
            dic.append(newd)
            #return "hello world"

    if(len(dic)<=0):
        abort(204)
    return jsonify(dic), 200
"""

@app.route('/api/v1/categories/<categoryName>/acts/size',methods=['GET'])         #
def list_no_of_acts(categoryName):
    global crash
    if(crash!=0):
        abort(500)
    global total_reqs
    total_reqs+=1
    if(request.method != "GET"):
        abort(415)
    f=open("static/categories.txt","r")
    categories=f.readlines()
    categorie_names=[x.split('\t')[0] for x in categories]
    if(categoryName not in categorie_names):
        abort(400)
    else:
        for cate in categories:
            if(cate.split('\t')[0]==categoryName):
                return jsonify([int(cate.split('\t')[1][:-1])]), 200
    
    #return "hello world!"


@app.route('/api/v1/categories/<categoryName>/acts',methods=['GET'])         #
def list_no_of_act_in_range(categoryName):
    global crash
    if(crash!=0):
        abort(500)
    global total_reqs
    total_reqs+=1
    if(request.method != "GET"):
        abort(415)
    
    try:
        start = request.args['start']
        end= request.args['end']
    except:
        start=-1
        end=-1
 


    f=open("static/categories.txt","r")
    
    categories=f.readlines()
    categorie_names=[x.split('\t')[0] for x in categories]
    if(categoryName not in categorie_names):
        abort(400)
    f.close()

    f=open("static/acts_info.txt","r")
    acts=f.readlines()
    
    if(int(end)>len(acts) or int(start)>len(acts)):
        abort(400)

    if(int(end)-int(start)+1>100):
        abort(413)
    reqacts=[]
    for act in acts:
        if(act.split('\t')[1]==categoryName):
            st=""
            st+=(((act.split('\t')[5]).split(":")[0]).split("-")[2])
            st+=(((act.split('\t')[5]).split(":")[0]).split("-")[1])
            st+=(((act.split('\t')[5]).split(":")[0]).split("-")[0])
            st+=(((act.split('\t')[5]).split(":")[1]).split("-")[2])
            st+=(((act.split('\t')[5]).split(":")[1]).split("-")[1])
            st+=(((act.split('\t')[5]).split(":")[1]).split("-")[0])
            reqacts.append([act,st])


    def takeSecond(elem):
        return elem[1]

    reqacts=sorted(reqacts,reverse=True,key=takeSecond)

    if(int(start)==-1 and int(end)==-1):
        if(len(reqacts)>100):
            abort(413)
        elif(len(reqacts)==0):
            return "no content",204
        
        else:
            dic=[]

            for act in [x[0] for x in reqacts]:
                
                newd={}
                
                newd["actId"]=int(act.split('\t')[0])
                #return act.split('\t')[4]
                newd["username"]=act.split('\t')[3]
                newd["timestamp"]=act.split('\t')[5]
                newd["caption"]=act.split('\t')[2]
                newd["upvotes"]=int(act.split('\t')[6])
                newd["imgB64"]=act.split('\t')[7][:-1]
                dic.append(newd)

            return jsonify(dic), 200

    else:
        if(int(start)<1 or int(end)>len(reqacts)):
            abort(400)
        elif(len(end)-len(start)+1>100):
            abort(413)
        else:
            dic=[]
            k=0
            #return(jsonify([x[0] for x in reqacts]))
            for act in [x[0] for x in reqacts]:
                
                newd={}
                if(k>=int(start) and k<=int(end)):
                    newd["actId"]=act.split('\t')[0]
                    #return act.split('\t')[4]
                    newd["username"]=act.split('\t')[3]
                    newd["timestamp"]=act.split('\t')[5]
                    newd["caption"]=act.split('\t')[2]
                    newd["upvotes"]=act.split('\t')[6]
                    newd["imgB64"]=act.split('\t')[7][:-1]
                    dic.append(newd)
                k+=1

            if(len(dic)==0):
                return "no content",204
            
            return jsonify(dic), 200
    #return "hello world!"



@app.route('/api/v1/acts/upvote',methods=['POST'])       #
def upvote():
    global crash
    if(crash!=0):
        abort(500)
    global total_reqs
    total_reqs+=1
    if(request.method != "POST"):
        abort(415)
    data= request.get_json(force=True)
    
    act_to_upvote=str(data[0])
    #return str(act_to_upvote)
    f=open("static/acts_info.txt","r")
    acts=f.readlines()
    ids=[x.split('\t')[0] for x in acts]
    #return jsonify(ids)
    if(act_to_upvote not in ids):
        return "hello there"
        abort(400)
    else:
        reqact=""
        for act in acts:
            if(act.split('\t')[0]==act_to_upvote):
                reqact=act
                break
        new=""
        new_votes=int(reqact.split('\t')[6])+1
        req_act_arr=reqact.split('\t')
        req_act_arr[6]=str(new_votes)
        new='\t'.join(req_act_arr)
        acts[acts.index(reqact)]=new
        f.close()
        st="".join(acts)
        f=open("static/acts_info.txt","w")
        f.write(st)
        f.close()
    
    return "upvoted", 200


@app.route('/api/v1/acts/<actId>',methods=['DELETE'])    #
def remove_act(actId):
    global crash
    if(crash!=0):
        abort(500)
    global total_reqs
    total_reqs+=1
    if(request.method != "DELETE"):
        abort(415)
    f=open("static/acts_info.txt","r")
    acts=f.readlines()
    ids=[x.split('\t')[0] for x in acts]
    #return jsonify(acts)
    if(actId not in ids):
        abort(400)
    else:
        for act in acts:
            if(act.split('\t')[0]==actId):
                acts.remove(act)
                break
        f.close()
        f=open("static/acts_info.txt","w")
        f.write("".join(acts))
        f.close()
    return "removed", 200


@app.route('/api/v1/acts',methods=['POST'])
def upload_act():
    global crash
    if(crash!=0):
        abort(500)
    global total_reqs
    total_reqs+=1
    global acts_uploaded
    acts_uploaded+=1
    if(request.method != "POST"):
        abort(415)
    
    data= request.get_json(force=True)

    if(len(data)!=6):
        abort(400)

    actid=str(data['actId'])
    
    user=str(data['username'])
    timestamp=str(data['timestamp'])
    caption=str(data['caption'])
    categoryname=str(data['categoryName'])
    imgB64=str(data['imgB64'])


    for c in imgB64:
        if(not((c>='a' and c<='z') or (c>='A' and c<='Z') or (c>='0' and c<='9') or (c=='+') or (c=='/') or c=='=')):
            abort(400)
    """
    try:
        if type(sb) == str:
            sb_bytes = bytes(sb, 'ascii')
        elif type(sb) == bytes:
            sb_bytes = sb
    except Exception as e:
        abort(400)

    
    a=base64.b64decode(imgB64)
    f=open("a.jpeg","wb")
    try:
        f.write(a)
    except:
        abort(400)
    
    if(data[0]['upvotes']!= None):
        abort(400)
    """
    """
    f1=open("static/usernames.txt","r")
    names=[x.split("\t")[0] for x in f1.readlines()]
    if(user not in names):
        #return user
        abort(400)
    f1.close()
    """
    headers= {'Origin':'3.210.137.58'}
    r=requests.get('http://3.210.151.222:80/api/v1/users',headers=headers)
    if(r.status_code == 204):
        abort(400)
    dat=list(r.json())
    #
    if(user not in dat):
        #return user
        abort(400)

    #return "came here",200
    f2=open("static/categories.txt","r")
    cates=[x.split('\t')[0] for x in f2.readlines()]
    #return str(cates[0])
    if(categoryname not in cates):
        #return categoryname
        abort(400)
    f2.close()
    
    #return "came here",200
    """
    pasw=""
    f1=open("static/usernames.txt","r")
    creds=f1.readlines()
    #return jsonify(creds)
    for cred in creds:
        if(cred.split('\t')[0]==user):
            pasw=cred.split('\t')[1][:-1]
            break
    f1.close()
    

    r=requests.get('http://3.210.151.222:8080/api/v1/users2')
    dat=list(r.json())
    passw=""
    for cre in dat:
        if(cre[0]==user):
            passw+=cre[1][:-1]
            break
    """
    
    st=actid+"\t"+categoryname+"\t"+caption+"\t"+user+"\t"+"not to be here"+"\t"+timestamp+"\t0\t"+imgB64+"\n"
    f=open("static/acts_info.txt","r")
    acts=f.readlines()
    ids=[x.split('\t')[0] for x in acts]
    if(actid in ids):
        #return actid
        abort(400)

   # return str(len((timestamp.split(":")[0]).split("-")[1]))

    if(len((timestamp.split(":")[0]).split("-")[0])!=2 or len((timestamp.split(":")[0]).split("-")[1])!=2 or len((timestamp.split(":")[0]).split("-")[2])!=4):
        #return "hello"
        abort(400)
    if(len((timestamp.split(":")[1]).split("-")[0])!=2 or len((timestamp.split(":")[1]).split("-")[1])!=2 or len((timestamp.split(":")[1]).split("-")[2])!=2):
        #return "hello"
        abort(400)

    
    acts.append(st)
    newt="".join(acts)
    f.close()
    f=open("static/acts_info.txt","w")
    f.write(newt)
    f.close()
    
    return "uploaded!", 201



if __name__ == "__main__":
    app.debug=True
    #app.run(host="0.0.0.0",port=80)
    app.run(port = 5000)
