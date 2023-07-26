import re
from flask import Flask,render_template,request,session
import cv2
import os
from playsound import playsound
import mysql.connector
import re

app=Flask(__name__)
conn = mysql.connector.connect(user='sai', password='Saicheran',
                              host='localhost',
                              database='proj')
mycursor=conn.cursor()

print("connected")
weight=r"../project/yolov4-custom_last.weights"
config=r"../project/yolov4-custom.cfg"
classes=["Handgun","knife"]
net=cv2.dnn.readNet(weight,config)
model=cv2.dnn_DetectionModel(net)
model.setInputParams(scale=1/255,size=(416,416))
app.secret_key = 'super secret key'
@app.route('/')
def project():
    return render_template('main.html')

@app.route('/home')
def home():
    return render_template('main.html')

@app.route('/About')
def home1():
    return render_template('about.html')

@app.route('/login')
def login1():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def login():
    msg1=''
    if request.method=='POST':
        email=request.form["email"]
        password=request.form["password"]
        value1=[]
        value1.append(email)
        value1.append(password)
        value1tup=tuple(value1)
        sql2="SELECT * FROM new WHERE email=%s and password=%s"
        mycursor.execute(sql2,value1tup)
        account=mycursor.fetchone()
        if account is not None:
            session['Loggedin']=True
            session['id']=account[1]
            session['email']=account[1]
            return render_template('demo.html')
        else:
            msg1="Incorrect Email/password"
            return render_template('login.html',msg1=msg1)
    
    return render_template('login.html')
            
@app.route('/demo', methods=['POST'])
def demo():
    if request.method == 'POST':
        return render_template('demo.html')
    
    
@app.route('/register')
def signup1():
    return render_template('register.html')

@app.route('/contact')
def con():
    return render_template('contact.html')



@app.route("/register" ,methods=['POST'])
def signup():
    msg=''
    if request.method=='POST':
        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]
        sql = "SELECT * FROM new WHERE name=%s"
        mycursor.execute(sql,(name,))
        acc=mycursor.fetchone()
        if acc is not None:
            return render_template("login.html")
        else:
            value=[]
            value.append(name)
            value.append(email)
            value.append(password)
            valuetup=tuple(value)
            sql1 = "INSERT INTO new(name,email,password) VALUES(%s,%s,%s)"
        
            mycursor.execute(sql1,valuetup)
            conn.commit()
            msg="You have successfully registered!"
    return render_template('login.html',msg=msg)
@app.route('/image')
def img1():
    return render_template('image.html')

@app.route('/image',methods=["POST"])
def img():
    if request.method=='POST':
        f=request.files['file']
        basepath=os.path.dirname(os.path.abspath('application.py'))
     
        filepath=os.path.join(basepath,'uploads',f.filename)
       
        f.save(filepath)
        img=cv2.imread(filepath)
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        classID,scores,bboxes=model.detect(img,nmsThreshold=0.4,confThreshold=0.3)
        for classID,scores,bboxes in zip(classID,scores,bboxes):
            x,y,w,h=bboxes
            if scores>=0.7:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                cv2.putText(img,(classes[classID]+'accuracy:'+(str(round((scores*100),2)))+'%'),(x,y-10), cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
                cv2.putText(img,'Weapon Detected',(20,30),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),1)
        cv2.imshow('output',img)
        cv2.waitKey(0)
    cv2.destroyAllWindows()    
    return render_template("image.html")
@app.route('/video')
def vid1():
     return render_template("video.html")
@app.route('/video',methods=['POST'])
def vid():
    if request.method=='POST':
        f=request.files['file']
        basepath=os.path.dirname(os.path.abspath('application.py'))
        filepath=os.path.join(basepath,'uploads',f.filename)
        f.save(filepath)
        cap=cv2.VideoCapture(filepath)
        weapon=False
        while True:
            _, frame=cap.read()
            frame=cv2.resize(frame,(640,480))
            classID,scores,bboxes=model.detect(frame,nmsThreshold=0.4,confThreshold=0.5)
            for classID,scores,bboxes in zip(classID,scores,bboxes):
               x,y,w,h=bboxes
               cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
               cv2.putText(frame,(classes[classID]+'accuracy:'+(str(round((scores*100),2)))+'%'),(x,y-10),cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
               cv2.putText(frame,(classes[classID]+'Detected'),(20,30),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
               if scores>=0.7:
                weapon=True
            
            if weapon==True:
                cv2.imshow('video',frame)
            if cv2.waitKey(1) & 0xFF==ord('q'):
                break
    cv2.destroyAllWindows()          
    return render_template("video.html")
@app.route('/live')
def live1():
    return render_template("live.html")
@app.route('/live',methods=['POST'])
def live():
    if request.method=='POST':
        capp=cv2.VideoCapture(0)
        weapon=False
        while True:
            _, frame=capp.read()
            classID,scores,bboxes=model.detect(frame,nmsThreshold=0.4,confThreshold=0.3)
            for classID,scores,bboxes in zip(classID,scores,bboxes):
                x,y,w,h=bboxes
                if scores>=0.7:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
                    cv2.putText(frame,(classes[classID]+'accuracy:'+(str(round((scores*100),2)))+'%'),(x,y-10),cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
                    cv2.putText(frame,(classes[classID]+'Detected'),(20,30),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
            cv2.imshow('video',frame)
            if cv2.waitKey(1) & 0xFF==ord('q'):
                break
    capp.release()
    cv2.destroyAllWindows()
    return render_template("live.html")
        
        
if __name__ == '__main__':
    from werkzeug.serving import run_simple
    
   
    run_simple('localhost', 8080, app)


