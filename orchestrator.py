import requests
import sys
import base64
from flask import Flask, render_template, request, redirect, Response , abort, jsonify, make_response, Response
import random, json
from json import dumps
import binascii
from flask_cors import CORS
from time import sleep
import os
import math
import threading
import docker

s=requests.Session()
a=requests.adapters.HTTPAdapter(max_retries=1)
s.mount('http://',a)
port_to_be_fwd = 0
total_contnrs = 1
reqs = 0
flag=0
"""
def background():
    while(True):
        newc = background2()
        global total_contnrs
        global reqs
        reqs=0
        total_contnrs = newc
"""

def background():
    client = docker.from_env()
    global total_contnr
    global reqs
    global flag
    global total_contnrs
    timer=0
    while(True):
        if(flag == 1):
            for i in range(total_contnrs):

                url = 'http://127.0.0.1:'+str(8000+i)+'/api/v1/_health'
                try:
                    r=requests.get(url,stream=True)
                    """
                except:
                #    exit(0)
                    sleep(10)
                    print(i,"recurse")
                #    background()
                    """
                    if(r.status_code==500):
                        #os.system("sudo docker stop acts_",i,sep="")
                        print("removing bad server. Replacing with new server....")
                        name = 'acts_'+str(i)
                        container = client.containers.get(name)
                        container.stop()
                        #container.remove()
                        c2 = client.containers.run("surajsj/acts", detach=True, ports={8000:8000+i}, volumes={'acts_data':{'bind':'/usr/bin/static', 'mode':'rw'}})
                        container.remove()
                        c2.rename(name)
                        #os.system("sudo docker run --name acts_",i," -p 80:",(8000+i),"surajsj/acts",sep="")
                        print("done")
                except:
                    print("recurse",i)
                    sleep(10)

            sleep(1)

            timer+=1
            print(timer)
            if(timer%120 == 0):
                tc = math.floor(reqs/20) + 1
                print(tc)
                if(total_contnrs < tc):
                    for i in range(total_contnrs,tc):
                        #os.system("sudo docker stop acts_",i,sep="")
                        name = 'acts_'+str(i)
                        c2 = client.containers.run("surajsj/acts",detach=True, ports={8000:8000+i}, volumes={'acts_data':{'bind':'/usr/bin/static', 'mode':'rw'}})
                        c2.rename(name)
                        print("scaled up")
#                    return tc
                elif(total_contnrs > tc):
                    for i in range(tc,total_contnrs):
                        name = 'acts_'+str(i)
                        container = client.containers.get(name)
                        container.stop()
                        container.remove()
                    #    os.system("sudo docker run --name acts_",i," -p 80:",(8000+i),"surajsj/acts",sep="")
                        print("scaled down")
#                    return tc

                sleep(10)
                total_contnrs = tc
                reqs=0


app = Flask(__name__)
CORS(app)


@app.route('/api/v1/_health', methods=['GET'])
def health_check():
    global flag
    if(flag==0):
        flag=1
    global port_to_be_fwd
    global total_contnrs
    url = "http://127.0.0.1:"+str(8000+port_to_be_fwd)+"/api/v1/_health"
    r=requests.get(url)
    port_to_be_fwd=(port_to_be_fwd+1)%total_contnrs
    return "",r.status_code


@app.route('/api/v1/_crash', methods=['POST'])
def crash():
    global flag
    if(flag==0):
        flag=1
    
    global port_to_be_fwd
    global total_contnrs
    url = "http://127.0.0.1:"+str(8000+port_to_be_fwd)+"/api/v1/_crash"
    r=requests.post(url)
    port_to_be_fwd=(port_to_be_fwd+1)%total_contnrs
    return "",r.status_code


@app.route('/api/v1/_count', methods=['GET'])
def count():
    global flag
    if(flag==0):
        flag=1
    global reqs
    reqs = reqs+1
    
    global port_to_be_fwd
    global total_contnrs
    url = "http://127.0.0.1:"+str(8000+port_to_be_fwd)+"/api/v1/_count"
    r=requests.get(url)
    port_to_be_fwd=(port_to_be_fwd+1)%total_contnrs
    return jsonify(r.json()),r.status_code


@app.route('/api/v1/count', methods=['DELETE'])
def reset_count():
    global flag
    if(flag==0):
        flag=1
    global reqs
    reqs = reqs+1
    
    global port_to_be_fwd
    global total_contnrs
    url = "http://127.0.0.1:"+str(8000+port_to_be_fwd)+"/api/v1/count"
    r=requests.delete(url)
    port_to_be_fwd=(port_to_be_fwd+1)%total_contnrs
    return "",r.status_code


@app.route('/api/v1/acts/count', methods=['GET'])
def get_no_of_acts_uploaded():
    global flag
    if(flag==0):
        flag=1
    global reqs
    reqs = reqs+1
    global port_to_be_fwd
    global total_contnrs
    url = "http://127.0.0.1:"+str(8000+port_to_be_fwd)+"/api/v1/acts/count"
    r=requests.get(url)
    port_to_be_fwd=(port_to_be_fwd+1)%total_contnrs
    return jsonify(r.json()),r.status_code


@app.route('/api/v1/categories', methods=['GET'])
def get_categories():
    global flag
    if(flag==0):
        flag=1
    global reqs
    reqs = reqs+1
    
    global port_to_be_fwd
    global total_contnrs
    url = "http://127.0.0.1:"+str(8000+port_to_be_fwd)+"/api/v1/categories"
    r=requests.get(url)
    port_to_be_fwd=(port_to_be_fwd+1)%total_contnrs
    if(r.status_code!=204):
        return jsonify(r.json()),r.status_code
    else:
        return "",r.status_code

@app.route('/api/v1/categories', methods=['POST'])
def set_category():
    global flag
    if(flag==0):
        flag=1
    global reqs
    reqs = reqs+1
    
    global port_to_be_fwd
    global total_contnrs
    data= request.get_json(force=True)
    print(data[0])
    y=json.dumps(list(data[0]))

    url = "http://127.0.0.1:"+str(8000+port_to_be_fwd)+"/api/v1/categories"
    r=requests.post(url, data = y)
    port_to_be_fwd=(port_to_be_fwd+1)%total_contnrs
    return "",r.status_code


@app.route('/api/v1/categories/<categoryName>', methods=['DELETE'])
def delete_category(categoryName):
    global flag
    if(flag==0):
        flag=1
    global reqs
    reqs = reqs+1
    
    global port_to_be_fwd
    global total_contnrs
    url = "http://127.0.0.1:"+str(8000+port_to_be_fwd)+"/api/v1/categories/"+str(categoryName)
    r=requests.delete(url)
    port_to_be_fwd=(port_to_be_fwd+1)%total_contnrs
    return "",r.status_code


@app.route('/api/v1/categories/<categoryName>/acts/size', methods=['GET'])
def no_of_acts(categoryName):
    global flag
    if(flag==0):
        flag=1
    global reqs
    reqs = reqs+1
    
    global port_to_be_fwd
    global total_contnrs
    url = "http://127.0.0.1:"+str(8000+port_to_be_fwd)+"/api/v1/categories/"+str(categoryName)+"/acts/size"
    r=requests.get(url)
    port_to_be_fwd=(port_to_be_fwd+1)%total_contnrs
    return jsonify(r.json()),r.status_code


@app.route('/api/v1/categories/<categoryName>/acts', methods=['GET'])
def get_acts(categoryName):
    global flag
    if(flag==0):
        flag=1
    global reqs
    reqs = reqs+1
    
    global port_to_be_fwd
    global total_contnrs
    url = "http://127.0.0.1:"+str(8000+port_to_be_fwd)+"/api/v1/categories/"+str(categoryName)+"/acts"
    r=requests.get(url)
    port_to_be_fwd=(port_to_be_fwd+1)%total_contnrs
    if(r.status_code!=204):
        return jsonify(r.json()),r.status_code
    else:
        return "",r.status_code

@app.route('/api/v1/acts/upvote', methods=['POST'])
def upvote():
    global flag
    if(flag==0):
        flag=1
    global reqs
    reqs = reqs+1
    data = request.get_json(force=True)
    y=json.dumps(list(data[0]))

    global port_to_be_fwd
    global total_contnrs
    url = "http://127.0.0.1:"+str(8000+port_to_be_fwd)+"/api/v1/acts/upvote"
    r=requests.post(url, data=y)
    port_to_be_fwd=(port_to_be_fwd+1)%total_contnrs
    return "",r.status_code


@app.route('/api/v1/acts/<actId>', methods=['DELETE'])
def delete_act(actId):
    global flag
    if(flag==0):
        flag=1
    global reqs
    reqs = reqs+1
    
    global port_to_be_fwd
    global total_contnrs
    url = "http://127.0.0.1:"+str(8000+port_to_be_fwd)+"/api/v1/acts/"+str(actId)
    r=requests.delete(url)
    port_to_be_fwd=(port_to_be_fwd+1)%total_contnrs
    return "",r.status_code


@app.route('/api/v1/acts', methods=['POST'])
def upload_act():
    global flag
    if(flag==0):
        flag=1
    
    data = request.get_json(force=True)
    #y=json.loads(data)
    z=json.dumps(data)
    global reqs
    reqs = reqs+1
    global port_to_be_fwd
    global total_contnrs
    url = "http://127.0.0.1:"+str(8000+port_to_be_fwd)+"/api/v1/acts"
    r=requests.post(url, data = z)
    port_to_be_fwd=(port_to_be_fwd+1)%total_contnrs
    return "",r.status_code





if __name__ == "__main__":

    t1 = threading.Thread(target = background)
    #t2 = threading.Thread(target = server)

    t1.start()
    
    app.debug=True
    app.run(host="0.0.0.0",port=80)
    sleep(2)

    t1.join()
    #t2.join()
    """
    global total_contnr
    global requests
    global flag
    global total_contnrs
    while(true):
        for i in range(total_contnr):
            r=requests.post('http://127.0.0.1:',(8000+i),'/api/v1/_health',sep="")
            if(r.status_code==500):
                os.system("sudo docker stop acts_",i,sep="")
                os.system("sudo docker run --name acts_",i," -p 80:",(8000+i),"surajsj/acts",sep="")
                

        time.sleep(1)
        if(flag == 1):
            timer+=1
            if(timer == 120):
                tc = math.floor(requests/20) + 1
                if(total_contnrs != tc):
                    for i in range(total_contnr):
                        os.system("sudo docker stop acts_",i,sep="")
                    for i in range(tc):
                        os.system("sudo docker run --name acts_",i," -p 80:",(8000+i),"surajsj/acts",sep="")
                    total_contnrs = tc
    """
    
