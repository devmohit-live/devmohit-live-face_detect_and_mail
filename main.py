'''
The Simple python program the uses OpenCV and smtplib that send the mail about the no of times
faces are detected with the times they detected
@author: Mohit Singh
@github: https://github.com/devmohit-live
@LinkedIN : https://www.linkedin.com/in/devmohitsingh/

'''

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import cv2 as cv
import datetime as dt

def face_dtetcor():
    times=[]
    count=0
    cap = cv.VideoCapture(0)
    facemodel=cv.CascadeClassifier("haarcascade_frontalface_default.xml")
    start=dt.datetime.now().minute
    while True: 
        st, frame = cap.read()
        faces=facemodel.detectMultiScale(frame)
        if(len(faces) > 0):
            for face in faces:
                x,y,w,h=face
                times.append(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                cv.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),5)

        frame=cv.putText(frame, str(len(faces))+' Faces detected',(50,50),cv.FONT_HERSHEY_SIMPLEX,0.75,[0,255,0],3)
        cv.imshow('Input', frame) 
        count+=len(faces)
        end=dt.datetime.now().minute
        if cv.waitKey(1) == 13 or end-start == 2 or end-start < 0 : # two minutes
            break 

    cv.destroyAllWindows()
    cap.release() 
    return((times,count))


def mailer(times,count):
    sender_email = "you mail id(sender)"
    receiver_email = "receivers mail id"
    # password = getpass.getpass()
    password = 'you mail password'

    message = MIMEMultipart("alternative")
    message["Subject"] = "Faces Found"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    try:
        text = """\
        Hey there , This is a message from Face-Recognition App
        """
        html = """\
        <html>
          <body>
            <p>Hi,<br>
               The app has detected some faces when your weren't there<br>
               The no. of faces detected are : <b>{}</b>
               <br>
               At times : <b>{}</b>
            </p>
          </body>
        </html>
        """.format(count,times)

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
    except e:
        print("Some error ocurred in mailer ! ",e)

if __name__ == "__main__":
    times,count = face_dtetcor()
    mailer(times,count)
    print('Succesfull!!!! ')