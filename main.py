import time
import numpy as np
import cv2
import smtplib
from email.message import EmailMessage
import datetime
from selenium import webdriver



def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    
    user = 'email.testing.01234@gmail.com'
    msg['from'] = user
    password = 'iskfjlgxghhcqmbf'
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

kernal_dil =np.ones((8,8), np.uint8)
#print(kernal_dil)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
#print(kernel)
fgbg = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=100, detectShadows=False)
#print(fgbg)

x = 650
y = 300
width = 500
height = 350



data_string= time.strftime("%d-%m-%H-%M-%S")
old_time = datetime.datetime.now()
old_time2 = datetime.datetime.now()
constant=0
try:
    while True:
        
        cap = cv2.VideoCapture('rtsp://admin:password@123@10.173.36.50/Streaming/Channels/1')
        ret, frame = cap.read()
        #fshape = frame.shape
    #     print(frame.shape)
        freq=0
        area_new=0
        frame = frame[500: 500 + 380, 500: 500 + 1020] #[y: y + height, x: x + width]
        if ret == True:
            blurFrame = cv2.GaussianBlur(frame,(5,5),0)
            fgmask = fgbg.apply(frame)
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
            dilation = cv2.dilate(fgmask, kernal_dil,iterations = 1)
            (contours,hierarchy) = cv2.findContours(dilation,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area>100):
    #                 print(area)
                    freq=freq+1
                    area_new=area_new+area
                    x,y,w,h = cv2.boundingRect(contour)
                    img=cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
                    roi_vehchile = frame[y: y + height, x: x + width]

            avg=area_new/freq
    #         print("end")
        
        new_time2=datetime.datetime.now()
        diff_time2 = new_time2 - old_time2
        if(diff_time2.total_seconds()>60 or constant == 0):
            driver = webdriver.Firefox(executable_path=r'C:\Users\Abhinv\Downloads\geckodriver.exe')
            old_time2 =datetime.datetime.now()
            driver.get("http://aqicn.org/city/india/gurgaon/vikas-sadan-gurgaon/")
            element = driver.find_element_by_id("aqiwgtvalue")
            aqi=element.text
            driver.close()
            constant=1
        else:
            pass
        
        data_string= time.strftime("%d-%m-%H-%M-%S")
        image_name = data_string+"_"+str(freq)+"_"+str(int(avg)).zfill(2) + "_" + str(aqi)
        cv2.imwrite('C:/data/'+ image_name  + ".jpg", frame)
        time.sleep(20)
        #cv2.imshow('original',frame)
        new_time=datetime.datetime.now()
        diff_time = new_time - old_time 
        if(diff_time.total_seconds()>7200):
            old_time =datetime.datetime.now()
            email_alert("WIP", str(new_time), "email.testing.01234@gmail.com")
        else:
            print("OK")
            pass
        
except Exception as e:
    email_alert("Internet working; error in process", str(e), "email.testing.01234@gmail.com")
    pass

#if cv2.waitKey(25) & 0xFF ==ord('q'):
#    break
cap.release()
#cv2.destroyAllWindows()


# In[15]:


import time
from selenium import webdriver
driver = webdriver.Firefox(executable_path=r'C:\Users\Abhinv\Downloads\geckodriver.exe')
#browser=webdriver.Firefox()
driver.get("http://aqicn.org/city/india/gurgaon/vikas-sadan-gurgaon/")
element = driver.find_element_by_id("aqiwgtvalue")
#title = element.getAttribute("title")
#l=driver.find_elements_by_class_name("aqivalue")
#element2 = driver.find_element_by_xpath("//form[input/@name ='search']")
#element=browser.find_element(By.ID,"searchinput")
#element.send_keys("typing")
print(element)
print(element.text)
time.sleep(3)
driver.close()