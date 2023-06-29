import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2, os
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time

IMAGE = 100
# ------------ functions ------------
# check and create path
def assure_path_exists(path):
    dir = os.path.dirname(path)
    if (not (os.path.exists(dir))):
        os.makedirs(dir)
# -----------------------------------
# get time
def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, tick)
# -----------------------------------
# auther info
def contact():
    mess._show(title='Contact Me', message="Please contact Me on : reza_adinepour@shahroodut.ac.ir ")
# -----------------------------------
# ckeck in directory, is there exist haarcascade file ?
def check_haarcascadefile():
    exists = os.path.isfile('haarcascade_frontalface_default.xml')
    if (exists):
        pass
    else:
        mess._show(title='Some file missing', message='Please contact Me for help')
        root.destroy()
# -----------------------------------
# save pasword in txt file
def save_pass():
    assure_path_exists('TrainingImageLabel' + os.sep)
    exists1 = os.path.isfile('TrainingImageLabel' + os.sep + 'psd.txt')
    if (exists1):
        tf = open('TrainingImageLabel' + os.sep + 'psd.txt', 'r')
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if(new_pas == None):
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open('TrainingImageLabel' + os.sep + 'psd.txt', 'w')
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if (newp == nnewp):
            txf = open('TrainingImageLabel' + os.sep + 'psd.txt', 'w')
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()
# -----------------------------------
# change password
def change_pass():
    global master
    master = tk.Tk()
    master.geometry('500x160')
    master.resizable(False, False)
    master.title('Change Password')
    master.configure(background='white')
    # Enter Old Password
    lbl4 = tk.Label(master, text='Enter Old Password', bg='white', font=('times', 12, 'bold'))
    lbl4.place(x=10, y=10)
    # Enter New Password box
    global old
    old = tk.Entry(master, width=25, fg='black', relief='solid', font=('times', 12, 'bold'), show='*')
    old.place(x=200, y=10)
    lbl5 = tk.Label(master, text='Enter New Password', bg='white', font=('times', 12, 'bold'))
    lbl5.place(x=10, y=45)
    # Confirm New Password box
    global new
    new = tk.Entry(master, width=25, fg='black', relief='solid', font=('times', 12, 'bold'), show='*')
    new.place(x=200, y=45)
    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=('times', 12, 'bold'))
    lbl6.place(x=10, y=80)
    # cancel button
    global nnew
    nnew = tk.Entry(master, width=25, fg='black', relief='solid', font=('times', 12, 'bold '), show='*')
    nnew.place(x=200, y=80)
    cancel=tk.Button(master, text='Cancel', command=master.destroy, fg='white', bg='#FA0505', height=1, width=25,
                      activebackground='#B80505', font=('times', 10, 'bold')) 
    cancel.place(x=220, y=120)
    # cancel button
    save1 = tk.Button(master, text='Save', command=save_pass, fg='white', bg='#10E706', height=1, width=25,
                       activebackground='#049C14', font=('times', 10, 'bold'))
    save1.place(x=10, y=120)

    master.mainloop()
# -----------------------------------
# box for enter password and train network
def psw():
    assure_path_exists("TrainingImageLabel" + os.sep)
    exists1 = os.path.isfile("TrainingImageLabel" + os.sep + "psd.txt")
    if (exists1):
        tf = open("TrainingImageLabel" + os.sep + "psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if (new_pas) == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel" + os.sep + "psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        progress_bar()
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')
# -----------------------------------  
# create progress bar     
def progress_bar():
    
    progress = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
    progress.place(x=920, y=600)  # set the x and y coordinates

    # create a label for showing the percentage progress
    percent_label = tk.Label(root, text='0%')
    percent_label.place(x=1225, y=600)  # set the x and y coordinates

    # define a function to update the progress bar
    def update_progress():
        for i in range(101):
            progress['value'] = i
            percent_label.config(text='{}%'.format(i))
            progress.update()
            root.after(70)  # delay in ms
    update_progress()
    # time.sleep(2)
    progress.destroy()
    percent_label.destroy()
# -----------------------------------
# clear command
def clear():
    txt.delete(0, 'end')
    res = '1)Take Images  >>>  2)Save Profile'
    message1.configure(text=res)
    
def clear2():
    txt2.delete(0, 'end')
    res = '1)Take Images  >>>  2)Save Profile'
    message1.configure(text=res)
# -----------------------------------
# taking image from user
def TakeImages():
    message1.configure(text='Starting...')
    check_haarcascadefile()
    columns = ['ID', '', 'NAME']
    assure_path_exists('StudentDetails' + os.sep)
    assure_path_exists('TrainingImage' + os.sep)
    exists = os.path.isfile('StudentDetails' + os.sep + 'StudentDetails.csv')
    if (exists):
        pass
    else:
        with open('StudentDetails' + os.sep + 'StudentDetails.csv', 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # set Width
        cam.set(4, 480) # set Height
        harcascadePath = 'haarcascade_frontalface_default.xml'
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                # incrementing sample number
                sampleNum += 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite('TrainingImage' + os.sep + name + '.' + Id + '.' + str(sampleNum) + '.jpg',
                            gray[y:y + h, x:x + w])
                # cv2.imwrite('TrainingImage' + os.sep + name + '.' + Id + '.' + str(sampleNum) + '.jpg',
                #             gray[y:y + h, x:x + w])
                # display the frame
                cv2.imshow('Taking Images', img)
                # print('image {} was taken'.format(sampleNum))
            # wait for 100 miliseconds
            if (cv2.waitKey(100) & 0xFF == 27):
                break
            # break if the sample number is morethan 100
            elif (sampleNum >= IMAGE):
                break
        cam.release()
        cv2.destroyAllWindows()
        res = 'Images Taken for ID : ' + Id
        row = [Id, '', name]
        with open('StudentDetails' + os.sep + 'StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = 'Enter Correct name'
            message.configure(text=res)
# -----------------------------------
# train phase
def TrainImages():
    check_haarcascadefile()
    assure_path_exists('TrainingImageLabel' + os.sep)
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = 'haarcascade_frontalface_default.xml'
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels('TrainingImage')
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save('TrainingImageLabel' + os.sep + 'Trainner.yml')
    res = 'Profile Saved Successfully'
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(max(ID)))
# -----------------------------------
# get images and lables
def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split('.')[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids
# -----------------------------------
# test phase
def TrackImages():
    check_haarcascadefile()
    assure_path_exists('Attendance' + os.sep)
    assure_path_exists('StudentDetails' + os.sep)
    for k in tv.get_children():
        tv.delete(k)
    # msg = ''
    i = j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # or cv2.createLBPHFaceRecognizer()
    exists3 = os.path.isfile('TrainingImageLabel' + os.sep + 'Trainner.yml')
    if (exists3):
        recognizer.read('TrainingImageLabel' + os.sep + 'Trainner.yml')
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = 'haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set Width
    cam.set(4, 480) # set Height
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile('StudentDetails' + os.sep + 'StudentDetails.csv')
    if (exists1):
        df = pd.read_csv('StudentDetails' + os.sep + 'StudentDetails.csv')
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        root.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)
            # serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                # aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                # D = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                aa = df.loc[df['ID'] == Id]['NAME'].values
                ID = df.loc[df['ID'] == Id]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]
            else:
                Id = bb = 'Unknown'
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                # aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                # ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                attendance = [0, '', bb, '', str(date), '', str(timeStamp)]
                bb = str(Id)
            cv2.putText(im, str('{}%'.format(round(100 - conf))), (x + 5, y + h - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(im, str(bb), (x, y), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        k = cv2.waitKey(1) & 0xFF

        if (k == 27):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile('Attendance' + os.sep + 'Attendance_' + date + '.csv')
    if (exists):
        with open('Attendance' + os.sep + 'Attendance_' + date + '.csv', 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open('Attendance' + os.sep + 'Attendance_' + date + '.csv', 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
    with open('Attendance' + os.sep + 'Attendance_' + date + '.csv', 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i += 1
            if (i > 1):
                if ((i % 2) != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text='      ' + iidd, values=('            ' + str(lines[2]),
                                                                   '            ' + str(lines[4]),
                                                                   '              ' + str(lines[6])) )
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()
# -----------------------------------
# convert calendar
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day, month, year = date.split("-")

mont = { '01':'January',
         '02':'February',
         '03':'March',
         '04':'April',
         '05':'May',
         '06':'June',
         '07':'July',
         '08':'August',
         '09':'September',
         '10':'October',
         '11':'November',
         '12':'December' }
# -----------------------------------
# GUI user interface
root = tk.Tk()
# get size of monitor
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(str(screen_width)+'x'+str(screen_height)) # set size

root.resizable(False, False) # user cant resize app
root.title("Attendance System") # Set the title of the window
root.configure(background='#282523') # set color of the background
root.iconbitmap('image/icon_app.ico') # Set the icon of the window

# add logo
logo = Image.open('image' + os.sep + 'logo.png') # Load the image file
logo_image = ImageTk.PhotoImage(logo) # create a Tkinter-compatible photo image
logo_label = tk.Label(root, image=logo_image)
logo_label.place(x=0, y=0) # set position of the logo
logo_label.lift() # Bring the logo label to the foreground

# seting of 2 main box
frame1 = tk.Frame(root, bg='#F9ECEC')
frame1.place(relx=0.11, rely=0.17, relwidth=0.38, relheight=0.70)
frame2 = tk.Frame(root, bg='#F9ECEC')
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.70)

# setting of top text
message3 = tk.Label(root, text='Face Recognition Based Attendance System', fg="white", 
                    bg='#282523', width=35, height=1, font=('times', 29, 'bold') )
message3.place(x=380, y=10)

# setting of time and calender
frame3 = tk.Frame(root, bg="#c4c6ce")
frame3.place(relx=0.51, rely=0.09, relwidth=0.1, relheight=0.07)

frame4 = tk.Frame(root, bg="#c4c6ce")
frame4.place(relx=0.36, rely=0.09, relwidth=0.155, relheight=0.07)

datef = tk.Label(frame4, text=day + '-' + mont[month] + '-' + year + '    |', fg='orange', 
                 bg='#262523', width=55, height=1, font=('times', 22, 'bold') )
datef.pack(fill='both', expand=1)

clock = tk.Label(frame3, fg='orange', bg='#262523', width=55, height=1, font=('times', 22, 'bold') )
clock.pack(fill='both', expand=1)
tick()

head2 = tk.Label(frame2, text='                             For New Registrations                              ',
                  fg='black', bg='#3ece48', font=('times', 17, 'bold') )
head2.grid(row=0,column=0)

head1 = tk.Label(frame1, text='                            For Already Registered                              ',
                  fg='black', bg='#3ece48', font=('times', 17, 'bold') )
head1.place(x=0,y=0)

lbl = tk.Label(frame2, text='Enter ID', width=20 , height=1 , fg='black' , bg='#C2D4FF', font=('times', 17, 'bold') )
lbl.place(x=140, y=55)

txt = tk.Entry(frame2, width=35, fg='black', font=('times', 15, 'bold') )
txt.place(x=70, y=88)

lbl2 = tk.Label(frame2, text='Enter Name', width=20, fg='black', bg='#C2D4FF', font=('times', 17, 'bold') )
lbl2.place(x=140, y=140)

txt2 = tk.Entry(frame2, width=35, fg='black', font=('times', 15, 'bold') )
txt2.place(x=70, y=173)

message1 = tk.Label(frame2, text='hint: 1) Take Images  =>  2) Save Profile', bg='#F9ECEC', fg='black', 
                    width=49, height=1, activebackground='yellow', font=('times', 15, 'bold') )
message1.place(x=-3, y=240)

message = tk.Label(frame2, text='', bg='#C2D4FF', fg='black', width=39, height=1, activebackground='yellow', 
                   font=('times', 16, 'bold') )
message.place(x=52, y=500)

lbl3 = tk.Label(frame1, text='Attendance', width=20, fg='black', bg='#C2D4FF', height=1, font=('times', 17, 'bold') )
lbl3.place(x=150, y=115)
# -----------------------------------

res=0
exists = os.path.isfile('StudentDetails' + os.sep + 'StudentDetails.csv')
if (exists):
    with open('StudentDetails' + os.sep + 'StudentDetails.csv', 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text='Total Registrations till now  : '+str(res))
# -----------------------------------

# menubar
menubar = tk.Menu(root, relief='ridge')
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='Change Password', command=change_pass)
filemenu.add_command(label='Contact Me', command=contact)
filemenu.add_command(label='Exit', command=root.destroy)
menubar.add_cascade(label='Help', font=('times', 29, 'bold'), menu=filemenu)
# -----------------------------------

# treeview attendance table
tv= ttk.Treeview(frame1, height=15, columns=('name','date','time'))
tv.column('#0', width=82)
tv.column('name', width=130)
tv.column('date', width=133)
tv.column('time', width=133)
tv.grid(row=2, column=0, padx=(60, 0), pady=(150, 0), columnspan=4)
tv.heading('#0', text ='ID')
tv.heading('name', text ='NAME')
tv.heading('date', text ='DATE')
tv.heading('time', text ='TIME')
# -----------------------------------

# scrollba
scroll=ttk.Scrollbar(frame1, orient='vertical', command=tv.yview)
scroll.grid(row=2, column=4, padx=(0, 100), pady=(250, 0), sticky='ns')
tv.configure(yscrollcommand=scroll.set)
# -----------------------------------

# buttons
clearButton = tk.Button(frame2, text='Clear', command=clear , fg='white', bg='#FF1414', bd=3,
                        width=11, activebackground='#D42525', font=('times', 11, 'bold') )
clearButton.place(x=425, y=86)

clearButton2 = tk.Button(frame2, text='Clear', command=clear2, fg='white', bg='#FF1414', bd=3,
                         width=11, activebackground='#D42525', font=('times', 11, 'bold') )
clearButton2.place(x=425, y=172)

takeImg = tk.Button(frame2, text='Take Images', command=TakeImages, fg='white', bg='#C4A053', bd=3,
                    width=34, height=1, activebackground='#A58747', font=('times', 15, 'bold') )
takeImg.place(x=80, y=300)

trainImg = tk.Button(frame2, text='Save Profile', command=psw, fg='white', bg='#C4A053', width=34, bd=3,
                     height=1, activebackground='#A58747', font=('times', 15, 'bold'))
trainImg.place(x=80, y=380)

trackImg = tk.Button(frame1, text='Take Attendance', command=TrackImages, fg='black', bg='#FFFA11', bd=3,
                     width=35,  height=1, activebackground='#E6E112', font=('times', 15, 'bold') )
trackImg.place(x=75, y=50)

quitWindow = tk.Button(frame1, text='Quit', command=root.destroy, fg='white', bg='#FF1414', width=35, bd=3,
                       height=1, activebackground='#D42525', font=('times', 15, 'bold') )
quitWindow.place(x=80, y=495)

root.configure(menu=menubar)
root.mainloop()
# -----------------------------------
# end