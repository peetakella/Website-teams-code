from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import matplotlib
from time import sleep
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import time #i2c ~~
import math
import smbus
import RPi.GPIO as GPIO #io~~
import matplotlib.pyplot as plt #graphing
import pygame
import threading
import pexpect
##print ('Imoprts done')



#Initialise Variables------------------------------------------------------------------------------------------------------------------------------------------------------

pygame.mixer.init()

# Fonts and texts
largetitletext = 105
mediumtitletext = 80
smalltitletext = 70
largetext=55
mediumtext = 30
smalltext = 25

window = 1

x1=0
x2=0
x3=0
x4=0
x5=0
x6=0
x7=0
x8=0
x9=0
x10=0
x11=0
x12=0
x13=0
x14=0
x15=0
x16=0
x17=0
x18=0
P=1
#Initialise Variables-------------------------------------------------------------------------------------------------------------------------------------------------









def open_sim_window():
    #print('open sim window')
    global window , L, P
    window = 4
    L=0
    P=1
    display_window()
    thd1 = threading.Thread(target=Background)
    thd1.daemon = True
    thd1.start()
    #print('end of open sim window')
    
def open_scenario_window():
    #print('Open Scenereo Window Functin')
    global window
    window = 3
    display_window()
    ##print ('window = ', window)
def open_home_window():
    #print('Open home Window Functin')
    global window, L, P
    window = 1
    L=0
    P=1
    display_window()
    ##print ('window = ', window)    
def open_data_window():
    #print('Open data Window Functin')    
    global window
    window = 2
    display_window()
    ##print ('window = ', window)
def View_Fail():
    #print('View Fail')    
    global window
    window = 5
    pygame.mixer.music.stop()
    display_window()
def View_Succede():
    #print('View succede')    
    global window
    window = 6
    pygame.mixer.music.stop()
    display_window()    
def View_Graph():
    #print('View print')    
    global window
    window = 7
    display_window()



def update_wound():
    # Update the 'wound' variable when a radiobutton is selected
    print("Wound:", wound.get())

def update_sound():
    # Update the 'sound' variable when a radiobutton is selected
    print("Sound:", sound.get())

def update_blood():
    # Update the 'blood' variable when a radiobutton is selected
    print("Blood:", blood.get())


def end(event4):
    #print('View end')    
    if event4.state == 1:
        View_Fail()
    else:
        View_Succede()


    
    

def display_window():
    print('Display window')
    # Destroy all widgets in the current frame
    for widget in frame.winfo_children():
        widget.destroy()
        
    if window == 3:
        #print('if window = 3')
        global wound, sound, blood
        wound = IntVar()  # Variable for wound choice
        sound = IntVar()  # Variable for sound choice
        blood = IntVar()  # Variable for blood choice

        #Add Title frame
        framet = LabelFrame(frame,fg="black", bg="gray75")
        framet.place(x=.025*w, y=.025*h, height=.2*h, width=.95*w)    
        # Add a label at the top of the window
        label_scenario = Label(framet, text="Choose Scenario", font=("Arial", largetitletext), fg="black", bg="gray75", pady = 15)
        label_scenario.pack(fill = X)
        
        #Add the Frames
        #Add left frame
        frameL = LabelFrame(frame,bg="firebrick3", fg="white")
        frameL.place(x=.015*w, y=.25*h, height=.675*h, width=.3*w)     
        #Add Middle frame
        frameM = LabelFrame(frame, padx=50, pady=5,bg="firebrick3", fg="white")
        frameM.place(x=.345*w, y=.25*h, height=.325*h, width=.3*w)            
        #Add Right Frame
        frameR = LabelFrame(frame, padx=50, pady=5,bg="firebrick3", fg="white")
        frameR.place(x=.675*w, y=.25*h, height=.675*h, width=.3*w)

        # Add the left section with wound choice checkboxes
        label_wound_choice = Label(frameL, text="Mode:", bg="firebrick3", fg="white",font=("Arial", largetitletext), padx= 40)
        label_wound_choice.grid(row=0, column=0, pady=0)    
        # Add the checkboxes for wound choice
        #wound = 1  #1=upper and 2=lower  
        checkbox_junction = Radiobutton(frameL, text="Packing",font=("Arial", smalltitletext), variable = wound, value=1,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=65, indicatoron=0,bd=10, command=update_wound)
        checkbox_junction.grid(row=1, column=0,padx=40, pady=20)
        checkbox_armT = Radiobutton(frameL, text="Tourniquet",font=("Arial", smalltitletext), variable = wound, value=2,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=11, indicatoron=0,bd=10, command=update_wound)
        checkbox_armT.grid(row=2, column=0,padx=40,pady=20)
        checkbox_armDP = Radiobutton(frameL, text="Pressure",font=("Arial", smalltitletext), variable = wound, value=3,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=45, indicatoron=0,bd=10, command=update_wound)
        checkbox_armDP.grid(row=3, column=0,padx=40,pady=20)        
        
        # Add the middle section with sound toggle switch
        label_sound = Label(frameM, text="Sound:", font=("Arial", largetitletext),bg="firebrick3", fg="white")
        label_sound.grid(row=0, column=0,columnspan=2, pady=0)    
        # Add the sound toggle switch
        #sound = 2
        checkbox_on = Radiobutton(frameM, text="On",font=("Arial", mediumtitletext), variable=sound, value=1,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=10, indicatoron=0,bd=10, command=update_sound)
        checkbox_on.grid(row=1, column=0,padx=0, pady=0)
        checkbox_off = Radiobutton(frameM, text="Off",font=("Arial", mediumtitletext), variable=sound, value=2,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=5, indicatoron=0,bd=10, command=update_sound)
        checkbox_off.grid(row=1, column=1,padx=0,  pady=0)
        
        #Button to enter scenario in middle frame
        button_scenario = Button(frame, text="Begin", command = lambda: [open_sim_window()],  font=("Arial", largetitletext),bg="firebrick3",fg="white")
        button_scenario.place(x=.345*w, y=.6*h, height=.15*h, width=.3*w)
        button_quit = Button(frame, text="Home", command = lambda: [open_home_window()],  font=("Arial", largetitletext),bg="firebrick3",fg="white")
        button_quit.place(x=.345*w, y=.775*h, height=.15*h, width=.3*w)

        # Add the right section with bleed out time checkboxes
        label_bleed = Label(frameR, text="Blood:", font=("Arial", largetitletext),bg="firebrick3", fg="white")
        label_bleed.grid(row=0, column=0, pady=0)
        # Add the checkboxes for bleed out time
        #blood = 3
        checkbox_high = Radiobutton(frameR, text="High",font=("Arial", mediumtitletext), variable=blood, value=1,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=110, indicatoron=0,bd=10, command=update_blood)
        checkbox_high.grid(row=1, column=0,padx=0, pady=10)
        checkbox_low = Radiobutton(frameR, text="Low",font=("Arial", mediumtitletext), variable=blood, value=2,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=125, indicatoron=0,bd=10, command=update_blood)
        checkbox_low.grid(row=2, column=0,padx=0,  pady=10)
        checkbox_off = Radiobutton(frameR, text="Off",font=("Arial", mediumtitletext), variable=blood, value=3,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=150, indicatoron=0,bd=10, command=update_blood)
        checkbox_off.grid(row=3, column=0,padx=0,  pady=10)
            
    
    
    elif window == 1: 
        print('if window = 1')
        #Add Title frame        
        frame1 = LabelFrame(frame, pady=25, fg="black", bg="gray75")
        frame1.place(x=.025*w, y=.025*h, height=.2*h, width=.95*w)

        # Add a label at the top of the window
        label_home = Label(frame1, text="Hemorrhage Control Trainer", font=("Arial", largetitletext), fg="black", bg="gray75")
        label_home.pack(fill = X)
        # Add two buttons underneath the label of home page

        button_scenario = Button(frame, text="Choose\nScenario", command = lambda: [open_scenario_window()], bg="firebrick3",fg="white",  font=("Arial", largetitletext), padx=10, pady=200)
        button_scenario.place(x=.025*w, y=.25*h, height=.675*h, width=.47*w)
        button_retrieve = Button(frame, text="Retrieve\nData", command = lambda: [open_data_window()],bg="firebrick3",fg="white", font=("Arial", largetitletext), padx=10, pady=200)
        button_retrieve.place(x=.5025*w, y=.25*h, height=.675*h, width=.47*w)
        ##print('checkpoint 2')
        
    elif window == 2:
        #print('if window = 2')
        ##print('checkpoint 1')    
        global x, m, ma_x
        #configfile = Text(data_window, wrap=WORD, width=45, height= 20)
        x = []
        m = []
        ma_x = []
        #txtarea = Text(frame, width=40, height=20)
        #txtarea.grid(column = 0, row = 1)
        #txtarea.pack(pady=20)
        def browseFiles():
            filename = filedialog.askopenfilename(initialdir = "/home/stopthebleed/StoptheBleed", title = "Select a File", filetypes = (("Text files", "*.txt*"), ("all files", "*.*")))
            label_file_explorer.configure(text="File Opened: "+filename)    
            for line in open(filename, 'r'):
                data = [i for i in line.split()]
                x.append(float(data[0]))
                m.append(float(data[2]))            
            with open(filename, 'r') as f:
                #configfile.insert(INSERT, f.read())
                data = f.read()               
            pathh.insert(END, filename)
            #txtarea.insert(END, data)    
            #print(x[0:12])
            #print(m[0:12])    
            #filename.close()
            update_graph()
            x.clear()
            m.clear()
            return filename

        def update_graph():
            print('update graph')
            line.set_data(x, m)
            #line_20ref.setdata(x, )
            ax.relim()
            ax.autoscale_view()
            canvas.draw()
            #print(x[0:12])
            #print(m[0:12])

        frame1 = LabelFrame(frame, padx= 50, pady= 10, fg = 'black', bg = 'grey75')
        frame1.grid(row= 1, column= 1, columnspan= 1, padx= 25, pady= 20)

        pathh = Entry(frame)
        pathh.grid(column = 0, row = 3)
        #pathh.pack(side=LEFT, expand=True, fill=X, padx=20)

        label_file_explorer = Label(frame, text = "File Explorer using Tkinter", width = 100, height = 4, fg = "blue")
        label_file_explorer.grid(column = 0, row = 0, columnspan= 2)
          
        button_explore = Button(frame, text = "Browse Files", command = browseFiles)
        button_explore.grid(column = 0, row = 4)  

        button_exit = Button(frame, text = "Exit", command = exit)
        button_exit.grid(column = 0,row = 5)

        fig = Figure(figsize=(15, 8))
        ax = fig.add_subplot(111)
        line, = ax.plot(x, m)
        ax.grid()
        #line_20ref, = ax.plot(x. ma_x)

        canvas = FigureCanvasTkAgg(fig, master= frame1)
        canvas.draw()
        canvas.get_tk_widget().grid(column = 1, row = 1)
        
        '''#Add Title frame        
        frame1 = LabelFrame(frame, pady=25, fg="black", bg="gray75")
        frame1.place(x=.025*w, y=.025*h, height=.2*h, width=.95*w)

        # Add a label at the top of the window
        label_home = Label(frame1, text="Data Review", font=("Arial", largetitletext), fg="black", bg="gray75")
        label_home.pack(fill = X)
        # Add two buttons underneath the label of home page

        button_scenario = Button(frame, text="Enter", command = lambda: [browse_files()], bg="firebrick3",fg="white",  font=("Arial", largetitletext), padx=10, pady=200)
        button_scenario.place(x=.025*w, y=.25*h, height=.325*h, width=.47*w)
        button_retrieve = Button(frame, text="Go\nHome", command = lambda: [open_home_window()],bg="firebrick3",fg="white", font=("Arial", largetitletext), padx=10, pady=200)
        button_retrieve.place(x=.5025*w, y=.25*h, height=.325*h, width=.47*w)
        
        label_file_explorer = Label(frame, text = "File Explorer using Tkinter", width = 100, height = 4, fg = "blue")
        label_file_explorer.place(x=.5025*w, y=.58*h, height=.675*h, width=.47*w) 

        filename = filedialog.askopenfilename(initialdir = "/home/stopthebleed/StoptheBleed", title = "Select a File", filetypes = (("Text files", "*.txt*"), ("all files", "*.*")))
        label_file_explorer.configure(frame ,text="File Opened: "+filename)
        
        for line in open(filename, 'r'):
            data = [i for i in line.split()]
            x.append(float(data[0]))
            m.append(float(data[2]))            
        with open(filename, 'r') as f:
            #configfile.insert(INSERT, f.read())
            data = f.read()               
        pathh.insert(END, filename)
        #txtarea.insert(END, data)    
        #print(x[0:12])
        #print(m[0:12])    
        #filename.close()
        update_graph()    
        return filename'''



        
    elif window == 4:
        #print('if window = 4')        
        ##print ('wound', wound)
        ##print ('Sound', sound)
        ##print ('blood', blood)       
         
        bleedoutbarframe = LabelFrame(frame,bg="firebrick3", fg="white")
        bleedoutbarframe.grid(row=0, column=0)
        graphframe = LabelFrame(frame,bg="firebrick3", fg="white")
        graphframe.grid(row=0, column=1)
        
        # Add the frame that the bleedout bar will go in
        label_bleedoutbar = Label(bleedoutbarframe, text="Blood\nLost", bg="firebrick3", fg="white", font=("Arial", mediumtitletext), padx=70, pady=10)
        label_bleedoutbar.grid(row=0, column=0,columnspan=2, sticky="w")
        axis_bleedoutbar = Label(bleedoutbarframe, text='-    3.0\n\n-    2.5\n\n-    2.0\n\n-    1.5\n\n-    1.0\n\n-    0.5\n\n- 0.0 (L)', font=('Arial', 35), fg="white", bg="firebrick3")
        axis_bleedoutbar.grid(row=1, column = 1)
        progbar = ttk.Progressbar(bleedoutbarframe,length=750, orient="vertical", mode="determinate",takefocus=True, maximum=3)       
        progbar.grid(row=1, column=0, ipadx=130)
        #progbar.start
        progbar['value'] = 0
        ##print(3333333333333333333)    
       
       # Add the frame hat the graph will go in
        plt.rcParams.update({'font.size':22})
        fig = Figure(figsize=(15, 10.1))        
        global timelist,pressurelist,ma_xlist
        timelist = []
        pressurelist = []
        ma_xlist = []
            
        ax = fig.add_subplot(111)
        ax.set_title('Pressure', fontsize=80)
        ax.set_xlabel('Time (s)', fontsize=40)
        ax.set_ylabel('Pressure at Bleed (LBS)', fontsize=40)
        ax.set_xlim(-20, 20)
        ax.set_ylim(0, 30)
        line, = ax.plot(timelist, pressurelist, label='Your Pressure', linewidth=5, color = 'b')
        line_20ref, = ax.plot(timelist, ma_xlist, label='Target Pressure', linewidth=5, color = 'r' )
        ax.legend(loc='upper left', fontsize=20)
        
        # Add the canvas for the graph
        canvas_graph = FigureCanvasTkAgg(fig, master=graphframe)  # A tk.DrawingArea.
        canvas_graph.draw()
        canvas_graph.get_tk_widget().grid(row=1,column=0)
        
        def Update_Sim_Window(event1):
            #print('update sim window')
            ##print(event1.state)    
            big_BloodLost1 = float(event1.state)
            BloodLost1 = big_BloodLost1 / 1000000    
            ##print('BloodLost1:',BloodLost1)
            #BloodLost1=BloodLost1*200
            progbar['value'] = BloodLost1
            
        def Update_pressure(event2):
            #print('update pressure')
            ##print(event3.state)
            big_pressure = float(event2.state)
            smallpressure = big_pressure / 1000000    
            ##print('pressuregui:',smallpressure)            
            pressurelist.append(smallpressure)

            
        def Update_time(event3):
            #print('update time')
            ##print(event2.state)
            big_time = float(event3.state)
            smalltime = big_time / 1000000    
            #print('titaltime gui:',smalltime)            
            timelist.append(smalltime)
            ma_xlist.append(20)
            ax.set_xlim(smalltime - 30, smalltime + 10)  # Adjust the axis limits based on your data
            line, = ax.plot(timelist, pressurelist, label='Your Pressure', linewidth=5, color = 'b')
            line_20ref, = ax.plot(timelist, ma_xlist, label='Target Pressure', linewidth=5, color = 'r' )
            canvas_graph.draw()
     
        #print('pre root.bind')    
        root.bind("<<event1>>",Update_Sim_Window)
        root.bind("<<event2>>",Update_pressure)
        root.bind("<<event3>>",Update_time)     
        #print('post root.bind') 
     
    elif window == 5:
        print('if window = 5')
        #Add Title frame        
        frame1 = LabelFrame(frame, pady=25, fg="black", bg="gray75")
        frame1.place(x=.025*w, y=.025*h, height=.2*h, width=.95*w)
        # Add a label at the top of the window
        label_home = Label(frame1, text="You Failed", font=("Arial", largetitletext), fg="black", bg="gray75")
        label_home.pack(fill = X)
        # Add two buttons underneath the label of home page

        button_scenario = Button(frame, text="View\nGraph", command = lambda: [View_Graph()], bg="firebrick3",fg="white",  font=("Arial", largetitletext), padx=10, pady=200)
        button_scenario.place(x=.025*w, y=.25*h, height=.675*h, width=.47*w)
        button_retrieve = Button(frame, text="Go\nHome", command = lambda: [open_home_window()],bg="firebrick3",fg="white", font=("Arial", largetitletext), padx=10, pady=200)
        button_retrieve.place(x=.5025*w, y=.25*h, height=.675*h, width=.47*w)
        
    elif window == 6:
        print('if window = 6')        
        #Add Title frame        
        frame1 = LabelFrame(frame, pady=25, fg="black", bg="gray75")
        frame1.place(x=.025*w, y=.025*h, height=.2*h, width=.95*w)
        # Add a label at the top of the window
        label_home = Label(frame1, text="You Stopped The Bleed", font=("Arial", largetitletext), fg="black", bg="gray75")
        label_home.pack(fill = X)
        # Add two buttons underneath the label of home page

        button_scenario = Button(frame, text="View\nGraph", command = lambda: [View_Graph()], bg="firebrick3", fg="white", font=("Arial", largetitletext), padx=10, pady=200)
        button_scenario.place(x=.025*w, y=.25*h, height=.675*h, width=.47*w)
        button_retrieve = Button(frame, text="Go\nHome", command = lambda: [open_home_window()],bg="firebrick3",fg="white", font=("Arial", largetitletext), padx=10, pady=200)
        button_retrieve.place(x=.5025*w, y=.25*h, height=.675*h, width=.47*w)        

    elif window == 7:
        print('if window = 7')
        ##print ('wound', wound)
        ##print ('Sound', sound)
        ##print ('blood', blood)      
        #Add Title frame        
        button_home = Button(frame, text="Go\nHome", command = lambda: [open_home_window()],bg="firebrick3",fg="white", font=("Arial", largetext))
        button_home.place(x=0, y=.4*h, height=.2*h, width=.125*w)
        #Greate graph frame
        frame2 = Frame(frame, pady=25, bg="gray75")#.pack(fill=BOTH, expand = True)
        frame2.place(x=.125*w, y=0, height=h, width=.85*w)
        # Add a label at the top of the window
        #label_home = Label(frame1, text="Simulation Summary", font=("Arial", largetitletext), fg="black", bg="gray75")
        #label_home.pack(fill = X)
        
        #Add the frame hat the graph will go in
        plt.rcParams.update({'font.size':22})
        fig = Figure(figsize=(18, 10.1))        
        '''time = [0,1,2,3,4,5,6,7,8,9,10]
        pressure = [2,3,4,3,4,5,4,6,5,5,18]
        ma_x = [20,20,20,20,20,20,20,20,20,20,20]'''
           
        ax = fig.add_subplot(111)
        ax.set_title('Simulation Summary', fontsize=80)
        ax.set_xlabel('Time (s)', fontsize=40)
        ax.set_ylabel('Pressure at Bleed (LBS)', fontsize=40)
        ax.set_xlim(0, max(timelist) + 5)  # Adjust the axis limits based on your data
        ax.set_ylim(0, max(pressurelist) +5)
        line, = ax.plot(timelist, pressurelist, label='Your Pressure', linewidth=5, color = 'b')
        line_20ref, = ax.plot(timelist, ma_xlist, label='Target Pressure', linewidth=5, color = 'r' )
        ax.legend(loc='upper left', fontsize=20)
        
        # Add the canvas for the graph
        canvas_graph = FigureCanvasTkAgg(fig, master=frame2)  # A tk.DrawingArea.
        canvas_graph.draw()
        canvas_graph.get_tk_widget().pack(fill=BOTH, expand = True)       

            
        
            
            


        
root = Tk()
root.title("Better Bleeding Control")
##print ('main thread', threading.get_ident())
root.configure(bg="grey75")
#w = 1920
w=1920
h = 1050
root.geometry("{}x{}".format(w, h))
# Add Title frame
frame = Frame(root)
frame.pack(expand=True, fill=BOTH)
root.bind("<<event4>>",end)
# Initial content for the home window
display_window()
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#^^^^^GUI^^^         \/ \/ \/ Backend \/ \/ \/
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------













#------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------
#Sounds------------------------------------------------------------------------------------------------------------------------------------------------ 



sound1 = "/home/stopthebleed/StoptheBleed/Sounds/30seccondscream.mp3"
sound2 = "/home/stopthebleed/StoptheBleed/Sounds/30seccondscream.mp3"
sound3 = "/home/stopthebleed/StoptheBleed/Sounds/30seccondscream.mp3"
timestamp2 = 0
Falloffcount = 0
soundtimer = 0

#Sounds-------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
def Background():
    #print('enter background')
    while P == 1: #to make sure that the background loop runs when it is needed only
        #print('enter while loop')
        #sleep(.05)
        print('loop begin')
        global blood, wound, sound, L, timetostopthebleed
        if L == 0:
            #print('enter if L = 0')
            
            MAX_MOTOR_SPEED = 12000  # Initialize with a default value
            #name file to save data to
            '''name = input ("enter trial run name")
            filename=(f"{name}.txt")'''
            filename = (f"A - Previous Trial.txt")
            #TODO Throw error codes for when and if there is something that can't be in a file name and have them try again
            open(filename,"w")
            ##print (filename)
            tic3 = 0 #timestamp
            cycletime = 0
            ##print('1')
            tic1 = time.perf_counter()
            ##print('blood:',blood)
            if blood.get() == 1:     #2:30 also known as high
                MAX_MOTOR_SPEED = 14000
            if blood.get() == 2:     #5:00 also known as low
                MAX_MOTOR_SPEED = 2500
            ##print(MAX_MOTOR_SPEED)
            #if blood is 3, liquid is off

            timetostopthebleed = 1
            running_max = 0
            upthreshold1 = 20
            upthreshold2 = 20
            upthreshold3 = 20
            errorthreshold1 = 40
            errorthreshold2 = 40
            errorthreshold3 = 70


            #Motor speed value is set
            input_min = 0
            input_max1 = upthreshold1
            input_max2 = upthreshold2
            input_max3 = upthreshold3
            output_min = 100 #frequency in hz, higher is faster pumping
            output_max = MAX_MOTOR_SPEED

            # Calculate the ratio
            ratio1 = (output_max - output_min) / (input_max1 - input_min)
            ratio2 = (output_max - output_min) / (input_max2 - input_min)
            ratio3 = (output_max - output_min) / (input_max3 - input_min)
            

            totaltime = 0
            BloodLost = 0
            bus = smbus.SMBus(1) #I2C channel 1 is connected to the GPIO pins 2 (SDA) and 4 (SCL)
            STB_timer=0
            
            channel = 1          #select channel
            #set up digital io
            GPIO.setwarnings(False)           #do not show any warnings
            GPIO.setmode (GPIO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
            GPIO.setup(19,GPIO.OUT)       # initialize GPIO19 as an output, not important for the pressure sensor or load cell

            PUL = 12  #pwm pin
            DIR = 27  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
            ENA = 22  # Controller Enable Bit (High to Enable / LOW to Disable).

            GPIO.setmode(GPIO.BCM)
            GPIO.setup(PUL, GPIO.OUT)
            GPIO.setup(DIR, GPIO.OUT)
            GPIO.setup(ENA, GPIO.OUT)
            arm = 18
            junction = 4    
            GPIO.setup(arm, GPIO.OUT)
            GPIO.setup(junction, GPIO.OUT)
            p=GPIO.PWM(PUL, 100) #PWM Function is defined
            
            #Condition sensor for continuous measurements
            LOAD_SENSOR_ADDRESS1=0x28 #junction
            LOAD_SENSOR_ADDRESS2=0x27 #Higher arm sensor
            LOAD_SENSOR_ADDRESS3=0x26 #Lower arm sensor
            dummy_command=0x00
            offset=1000    
            #offset=int((input("Enter offset value, default 1000:") or 1000))                                        #subtracts zero offset per data sheet, should be 1000
            if wound.get() == 1:
                LOAD_SENSOR_DATA1=bus.read_byte(LOAD_SENSOR_ADDRESS1)#This apparently turns the load sensor on, only need it once
            elif wound.get() == 2:
                LOAD_SENSOR_DATA2=bus.read_byte(LOAD_SENSOR_ADDRESS2)
            elif wound.get() == 3:   
                LOAD_SENSOR_DATA3=bus.read_byte(LOAD_SENSOR_ADDRESS3)
            LBS_DATA_SENSOR1=0
            LBS_DATA_SENSOR2=0
            LBS_DATA_SENSOR3=0

            #Create empty lists
            data1 = []
            data2 = []
            data3 = []
            data4 = []

    #Set one time things-----------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    #Collect Data, if error happens continue until there are 5 errors in a row then quit---------------------------------------------------------------------------------------------------
        #print('presleep1')
        sleep(.005)
        #print('postsleep1')
        if wound.get() == 1:
            #print('enter if wound = 1 collect data')
            try :
                bus.write_byte(LOAD_SENSOR_ADDRESS1,dummy_command)#without this command, the status bytes go high on every other read
                LOAD_SENSOR_DATA1=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS1,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                ##print(3)
            except OSError:
                ##print('Error 1')
                sleep(.1)
                
                try :
                    LOAD_SENSOR_DATA1=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS1,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                except OSError:
                    ##print('Error 2')
                    sleep(.1)
                    
                    try :
                        LOAD_SENSOR_DATA1=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS1,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                    except OSError:
                        ##print('Error 3')
                        sleep(.1)
                
                        try :
                            LOAD_SENSOR_DATA1=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS1,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                        except OSError:
                            ##print('Error 4')
                            sleep(.1)
                            
                            try :
                                LOAD_SENSOR_DATA1=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS1,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                            except OSError:
                                ##print('Error 5')
                                ##print('Stopping Motor and Turning off Solenoids')
                                stop_pump()
                                sleep(5)
                                quit()
            
        elif wound.get() == 2:
            #print('enter if wound != 1 collect data')
            try :
                bus.write_byte(LOAD_SENSOR_ADDRESS1,dummy_command)#without this command, the status bytes go high on every other read
                LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                ##print(3)
            except OSError:
                ##print('Error 1')
                sleep(.1)
                
                try :
                    LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                except OSError:
                    ##print('Error 2')
                    sleep(.1)
                    
                    try :
                        LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                    except OSError:
                        ##print('Error 3')
                        sleep(.1)
                
                        try :
                            LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                        except OSError:
                            ##print('Error 4')
                            sleep(.1)
                            
                            try :
                                LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                            except OSError:
                                ##print('Error 5')
                                ##print('Stopping Motor and Turning off Solenoids')
                                stop_pump()
                                sleep(5)
                                quit()
        else:            
            try:
                bus.write_byte(LOAD_SENSOR_ADDRESS3,dummy_command)#without this command, the status bytes go high on every other read
                LOAD_SENSOR_DATA3=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS3,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                ##print(3)
            except OSError:
                ##print('Error 1')
                sleep(.1)
                
                try :
                    LOAD_SENSOR_DATA3=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS3,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                except OSError:
                    ##print('Error 2')
                    sleep(.1)
                    
                    try :
                        LOAD_SENSOR_DATA3=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS3,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                    except OSError:
                        ##print('Error 3')
                        sleep(.1)
                
                        try :
                            LOAD_SENSOR_DATA3=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS3,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                        except OSError:
                            ##print('Error 4')
                            sleep(.1)
                            
                            try :
                                LOAD_SENSOR_DATA3=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS3,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                            except OSError:
                                ##print('Error 5')
                                ##print('Stopping Motor and Turning off Solenoids')
                                stop_pump()
                                sleep(5)
                                quit()
                            
#Collect Data------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------
#Raw Data is turned into lbs and filtered----------------------------------------------------------------------------------------------------
        
        ##print('Raw sensor data 1:',LBS_DATA_SENSOR1)
        ##print('Raw sensor data 1:',LBS_DATA_SENSOR1)
        ##print('Raw sensor data 1:',LBS_DATA_SENSOR1)
        
        if wound.get() == 1:
            print('enter if wound = 1 filter data')
            LBS_DATA_SENSOR1=((LOAD_SENSOR_DATA1[0]&63)*2**8 + LOAD_SENSOR_DATA1[1] - offset)*100/14000                                                                                 #It does return the correct two bytes after the initial read byte command
            ##print ("Sensed load in LBS 1 = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA1[0]&63)*2**8 + LOAD_SENSOR_DATA1[1] - offset)*100/14000), "pounds")#plots out       
            LBS_DATA_SENSOR1 = 1 * LBS_DATA_SENSOR1
            if LBS_DATA_SENSOR1 < 0:
                LBS_DATA_SENSOR1 = 0
            elif LBS_DATA_SENSOR1 > 0 and LBS_DATA_SENSOR1 <= upthreshold1:  #upthreshpld line 300  
                STB_timer=0
            elif LBS_DATA_SENSOR1 > upthreshold1 and LBS_DATA_SENSOR1 <= errorthreshold1:
                LBS_DATA_SENSOR1 = upthreshold1
                STB_timer += cycletime
            else:
                LBS_DATA_SENSOR1 = 0
        elif wound.get() == 2:
            print('enter if wound = 1 filter data')
            LBS_DATA_SENSOR2=((LOAD_SENSOR_DATA2[0]&63)*2**8 + LOAD_SENSOR_DATA2[1] - offset)*100/14000                                                                                 #It does return the correct two bytes after the initial read byte command
            ##print ("Sensed load in LBS 1 = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA1[0]&63)*2**8 + LOAD_SENSOR_DATA1[1] - offset)*100/14000), "pounds")#plots out       
            LBS_DATA_SENSOR2 = 1 * LBS_DATA_SENSOR2
            if LBS_DATA_SENSOR2 < 0:
                LBS_DATA_SENSOR2 = 0
            elif LBS_DATA_SENSOR2 > 0 and LBS_DATA_SENSOR2 <= upthreshold2:  #upthreshpld line 300  
                STB_timer=0
            elif LBS_DATA_SENSOR2 > upthreshold2 and LBS_DATA_SENSOR2 <= errorthreshold2:
                LBS_DATA_SENSOR2 = upthreshold2
                STB_timer += cycletime
            else:
                LBS_DATA_SENSOR2 = 0
        else:
            print('enter if wound = 1 filter data')
            LBS_DATA_SENSOR3=((LOAD_SENSOR_DATA3[0]&63)*2**8 + LOAD_SENSOR_DATA3[1] - offset)*100/14000                                                                                 #It does return the correct two bytes after the initial read byte command
            ##print ("Sensed load in LBS 1 = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA1[0]&63)*2**8 + LOAD_SENSOR_DATA1[1] - offset)*100/14000), "pounds")#plots out       
            LBS_DATA_SENSOR3 = .66 * LBS_DATA_SENSOR3
            if LBS_DATA_SENSOR3 < 0:
                LBS_DATA_SENSOR3 = 0
            elif LBS_DATA_SENSOR3 > 0 and LBS_DATA_SENSOR3 <= upthreshold3:  #upthreshpld line 300  
                STB_timer=0
            elif LBS_DATA_SENSOR3 > upthreshold3 and LBS_DATA_SENSOR3 <= errorthreshold3:
                LBS_DATA_SENSOR3 = upthreshold3
                STB_timer += cycletime
            else:
                LBS_DATA_SENSOR3 = 0



#Raw Data is turned into lbs and filtered------------------------------------------------------------------------------------------------------------       
#----------------------------------------------------------------------------------------------------------------------------------------------------
#set motor Hz----------------------------------------------------------------------------------------------------------------------------------------            
        
        Hz1 = -(LBS_DATA_SENSOR1) * ratio1 + output_max
        ##print('Hz1:',Hz1)
        Hz2 = -(LBS_DATA_SENSOR2) * ratio2 + output_max #both arm pressure sensors data is added together to make the tourniquet/direct pressure setting
        #print('Hz2:',Hz2)
        Hz3 = -(LBS_DATA_SENSOR3) * ratio3 + output_max
        ##print('Hz3:',Hz3)

#Set motor Hz------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------
#Turn Motor on and update pwm----------------------------------------------------------------------------------------------------------------------------

        #print ('wound', wound.get())
        #print ('Sound', sound.get())
        #print ('blood', blood.get())
        
        if wound.get() == 1 and blood.get() <= 2:
            #print('enter motor set if wound = 1')
            #This Turns Relay On. 
            GPIO.output(junction, 1)
            #Motor is Enabled and frequency is set
            p.start(50) #PWM function is set to duty cycle of 50
            GPIO.output(DIR, GPIO.HIGH)      #set Directin to CCW 
            GPIO.output(ENA, GPIO.LOW)  #enable motor
            ##print('ENA set to LOW - Controller Enabled')
              
            p.ChangeFrequency(Hz1)            #Update motor speed to new value of Hz
            p.ChangeDutyCycle(50)
        
        elif wound.get() == 2 and blood.get() <= 2:
            #print('enter motor set if wound = 2')
            #print('Hz2', Hz2)
            #This Turns Relay On. 
            GPIO.output(arm, 1)
            #Motor is Enabled and frequency is set
            p.start(50) #PWM function is set to duty cycle of 50
            GPIO.output(DIR, GPIO.HIGH)      #set Directin to CCW 
            GPIO.output(ENA, GPIO.LOW)  #enable motor
            ##print('ENA set to LOW - Controller Enabled') 
            p.ChangeFrequency(Hz2)            #Update motor speed to new value of Hz
            p.ChangeDutyCycle(50)
            
        elif wound.get() == 3 and blood.get() <= 2:
            #print('enter motor set if wound = 3')
            #print('Hz3', Hz3)
            #This Turns Relay On. 
            GPIO.output(arm, 1)
            #Motor is Enabled and frequency is set
            p.start(50) #PWM function is set to duty cycle of 50
            GPIO.output(DIR, GPIO.HIGH)      #set Directin to CCW 
            GPIO.output(ENA, GPIO.LOW)  #enable motor
            ##print('ENA set to LOW - Controller Enabled') 
            p.ChangeFrequency(Hz3)            #Update motor speed to new value of Hz
            p.ChangeDutyCycle(50)                        

#Turn Motor on and update pwm----------------------------------------------------------------------------------------------------------------------------   
#-------------------------------------------------------------------------------------------------------------------------------------------------------      
#time keeping, cycle time total time and loop count-------------------------------------------------------------------------------------------------------
            
        tic4 = tic3
        ##print('tic4=',tic4)
        tic3 = time.perf_counter()
        ##print('tic3=',tic3)
        if tic4 == 0:
            tic4 = tic3 - .3
            ##print('tic4=',tic4)
        cycletime = tic3 - tic4
        ##print ('cycletime =:',cycletime, 'seconds')
        
        tic5 = time.perf_counter()
        totaltime = tic5-tic1
        ###print ('totaltime is', totaltime)
        ###print ('cycletime is', cycletime)
        #Count the times through the loop
        L+=1
        ###print('Loopcount =', L)
        
#time keeping, cycle time total time and loop count---------------------------------------------------------------------------        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Calculate Blood Loss-------------------------------------------------------------------------------------------------------------------------------------------------------
        if  wound.get() == 1:
            #print ('flow rate wound = 1')
            Flow_Rate = 0.2643*math.log(Hz1)-1.5221 #Liters per min
            BloodLost= BloodLost + (cycletime * Flow_Rate / 60)
            ###print('BloodLost is:', BloodLost, 'Liters')
        elif wound.get() == 2:
            #print ('flow rate wound = 2')
            Flow_Rate = 0.2643*math.log(Hz2)-1.5221 #Liters per min
            BloodLost= BloodLost + (cycletime * Flow_Rate / 60)
            ###print('BloodLost is:', BloodLost, 'Liters')          
        else:
            #print ('flow rate wound = 3')
            Flow_Rate = 0.2643*math.log(Hz3)-1.5221 #Liters per min
            BloodLost= BloodLost + (cycletime * Flow_Rate / 60)
            ###print('BloodLost is:', BloodLost, 'Liters')
            
        if BloodLost >= 3: #total blood lost to shut off machine, default is 3 (liters)
            #print('enter if bloodloss greater then 3') 
            stop_pump()
            ###print('You were not fast enough, your patient lost over 3 liters of blood and died')
            root.event_generate("<<event4>>", state=str(1))
            sleep(5)
            #quit() #TODO end thread and go back to home
            
        


#Calculate Blood Loss-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#STB timer reaches end------------------------------------------------------------------------------------------------------------------------------------------------------
        #print ('STB timer',STB_timer , 'timetostopthebleed' , timetostopthebleed)
        
        if STB_timer >= timetostopthebleed:
            #print('stb timer over timetostopbleed')
            stop_pump()
            #if sound.get() == 1:
            #    you_succeded.play()
                
            root.event_generate("<<event4>>", state=str(2)) 
            ##print('You Stopped the bleed')
            sleep(5)
            quit()    
                
                    
                    
#STB timer reaches end------------------------------------------------------------------------------------------------------------------------------------------------------                    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Add data to lists and save file--------------------------------------------------------------------------------------------------------------------------------------------

        data1.append(totaltime)
        data2.append(BloodLost)
        if wound.get() == 1:
            #print('enter set DATA if wound = 1')
            global DATA
            data3.append(LBS_DATA_SENSOR1)
            DATA = LBS_DATA_SENSOR1
        elif wound.get() == 2:
            #print('enter set DATA if wound = 2')
            data3.append((LBS_DATA_SENSOR2))
            DATA=(LBS_DATA_SENSOR2)
        else:
            print('enter set DATA if wound = 3')
            data3.append((LBS_DATA_SENSOR3))
            DATA=(LBS_DATA_SENSOR3)
        # Save the data to a file
        with open(filename, "a") as file:
            #print('enter writefile')
            #for d1, d2, d3 in zip(data1, data2, data3):
            file.write(f"{totaltime}\t{BloodLost}\t{DATA}\n")
            
#Add Data t list and save file-------------------------------------------------------------------------------------------------------------------------------            
#-------------------------------------------------------------------------------------------------------------------------------------------------------------            
#sound playing----------------------------------------------------------------------------------------------------------------------------------------------------------
        #print('Data1:',DATA)
        if sound.get()==1:
            #print('entersound')
            global timestamp2, Falloffcount, soundtimer
            #print('timer1:',soundtimer)
            timestamp1 = time.perf_counter()
            if timestamp2 == 0:
                timestamp1 = timestamp2
                #print('timestamp2=timestamp1')
            #print('timestamp1',timestamp1)
            #print('timestamp2',timestamp2)
            soundtimer = timestamp1-timestamp2
            #print('timer2:',soundtimer)
            if DATA >= 20 and soundtimer == 0:
                timestamp2 = time.perf_counter()
                #print ('falloffcount', Falloffcount)
                if Falloffcount in [0,3,6,9,12]:
                    print("play sound 1")
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("/home/stopthebleed/StoptheBleed/Sounds/30seccondscream.mp3")
                    pygame.mixer.music.set_volume(1.0)
                    pygame.mixer.music.play()                    
                    
                elif Falloffcount in [1,4,7,10,13]:
                    print("play sound 2")
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("/home/stopthebleed/StoptheBleed/Sounds/scream3.mp3")
                    pygame.mixer.music.set_volume(1.0)
                    pygame.mixer.music.play()
                  
                else:
                    print("play sound 3")
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("/home/stopthebleed/StoptheBleed/Sounds/getofflong.mp3")
                    pygame.mixer.music.set_volume(1.0)
                    pygame.mixer.music.play()
                    
            print('timer3:',soundtimer)        
            if DATA < 20 and DATA > 10 and soundtimer != 0:
                #print('Data 2:',DATA)
                Falloffcount += 1
                #print ("stop sounds")
                pygame.mixer.music.stop()
                pygame.mixer.music.load("/home/stopthebleed/StoptheBleed/Sounds/Moan1.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()
                timestamp2 = 0
            
            print('timer3:',soundtimer)        
            if DATA < 10 :
                #print('Data 2:',DATA)
                #Falloffcount += 1
                #print ("stop sounds")
                pygame.mixer.music.stop()              






#sound playing----------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#create events for GUI, pass Data------------------------------------------------------------------------------------------------------------------------------------
        rounded_BloodLost = round(BloodLost, 6)  # Rounds to 8 decimal places#TODO make string
        big_bloodLost = rounded_BloodLost*1000000
        int_BloodLost = int(big_bloodLost)
        #print('big_bloodlost:',int_BloodLost)  
        
        rounded_totaltime = round(totaltime, 6)  # Rounds to 8 decimal places
        big_totaltime = rounded_totaltime*1000000
        int_totaltime = int(big_totaltime)
        #print('big_totaltime:',int_totaltime)  
        
        rounded_DATA = round(DATA, 6)  # Rounds to 8 decimal places
        big_DATA = rounded_DATA*1000000
        int_DATA = int(big_DATA)
        #print('big_DATA:',int_DATA)
        
             
        root.event_generate("<<event1>>", state=str(int_BloodLost))     
        root.event_generate("<<event2>>", state=str(int_DATA))
        root.event_generate("<<event3>>", state=str(int_totaltime))  
        ##print('event generated')    
            
            

#create events for GUI, pass Data------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------       
#time refrence at the end of the cycle and loop count----------------------------------------------------------------------------------------------------------
        

        
#time refrence at the end of the cycle and loop count----------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------   
#stop pump and solenoid function-------------------------------------------------------------------------------------------------------------------------------     
        def stop_pump():
            print('enter stoppump')
            GPIO.output(ENA, GPIO.HIGH)
            GPIO.output(junction, 0)
            GPIO.output(arm,0)
            

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




root.mainloop()