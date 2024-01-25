"""
======================================================================================
Title:          gui.py
Authors:        Peter Keller, Jacob Schaef, Simon Swopes
Description:    GUI class for the better bleeding control application
Version:        2.0
==================================================================================
"""

from time import sleep
import tkinter as tk
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog

from src.events import *
from main import simulation, network, stateObserver

# Formating Constants
largetitletext = 105
mediumtitletext = 80
smalltitletext = 70
largetext=55
mediumtext = 30
smalltext = 25
w = 1920
h = 1080


#==================================================================================================
# Primary Class for GUI management
class Window:
    def __init__(self):
        self._state = 1
        self._root = Tk()

        # Simulation Options
        self._wound = IntVar()
        self._blood = IntVar()
        self._sound = IntVar()

        # Initialize Window
        self._root.title("Better Bleeding Control")
        self._root.configure(bg="gray75")
        self._root.geometry("{}x{}".format(w, h)) # Using size from version one
        self._frame = Frame(self._root)
        self._frame.pack(expand=True, fill=BOTH)
        self._root.bind("<<event4>>",end)

    #==================================================================================================
    # Method called in main loop
    def updateWindow(self):

        if self._state == 1:
            self.__DrawWindow1()
        elif self._state == 2:
            self.__DrawWindow2()
        elif self._state == 3:
            self.__DrawWindow3()
        elif self._state == 4:
            self.__DrawWindow4()
        elif self._state == 5:
            self.__DrawWindow5()
        elif self._state == 6:
            self.__DrawWindow6()
        elif self._state == 7:
            self.__DrawWindow7()
        elif self._state == 8:
            self.__DrawWindow8()
        else:
            raise ValueError("Invalid State")

        
        self._root.mainloop()

    # Destroy's previous window and changes state to new one to be drawn
    def _destroy_UpdateState(self, state):
        for widget in self._frame.winfo_children():
            widget.destroy()

        self._state = state
        stateObserver.state = state #Notifies all other objects


    #==================================================================================================
    # Drawing Methods

    # Home Window
    def __DrawWindow1(self):
        

        frame1 = LabelFrame(self._frame, pady=25, fg="black", bg="gray75")

        frame1.place(x=.025*w, y=.025*h, height=.2*h, width=.95*w)


        # Add a label at the top of the window
        label_home = Label(frame1, text="Hemorrhage Control Trainer", font=("Arial", largetitletext), fg="black", bg="gray75")
        label_home.pack(fill = X)



        # Add two buttons underneath the label of home page
        button_scenario = Button(self._frame, text="Choose\nScenario", command = lambda: [self._destroy_UpdateState(3)], bg="firebrick3",fg="white",  font=("Arial", largetitletext), padx=10, pady=200)
        button_scenario.place(x=.025*w, y=.25*h, height=.675*h, width=.47*w)
        button_retrieve = Button(self._frame, text="Retrieve\nData", command = lambda: [self._destroy_UpdateState(2)], bg="firebrick3",fg="white", font=("Arial", largetitletext), padx=10, pady=200)
        button_retrieve.place(x=.5025*w, y=.25*h, height=.675*h, width=.47*w)

    # Data Retrieval Window
    # TODO: acrtually draw graph
    def __DrawWindow2(self):
        x = []
        m = []
        ma_x = []

        def browseFiles():
            filename = filedialog.askopenfilename(initialdir = "/home/stopthebleed/StoptheBleed", title = "Select a File", filetypes = (("Text files", "*.txt*"), ("all files", "*.*")))
            label_file_explorer.configure(text="File Opened: "+filename)    
            for line in open(filename, 'r'):
                data = [i for i in line.split()]
                x.append(float(data[0]))
                m.append(float(data[2]))            
            with open(filename, 'r') as f:
                data = f.read()              
            pathh.insert(END, filename)
            update_graph()
            x.clear()
            m.clear()
            return filename

        frame1 = LabelFrame(self._frame, padx= 50, pady= 10, fg = 'black', bg = 'grey75')
        frame1.grid(row= 1, column= 1, columnspan= 1, padx= 25, pady= 20)

        pathh = Entry(self._frame)
        pathh.grid(column = 0, row = 3)

        label_file_explorer = Label(self._frame, text = "File Explorer using Tkinter", width = 100, height = 4, fg = "blue")
        label_file_explorer.grid(column = 0, row = 0, columnspan= 2)
         
        button_explore = Button(self._frame, text = "Browse Files", command = browseFiles)
        button_explore.grid(column = 0, row = 4)  

        button_exit = Button(self._frame, text = "Exit", command = exit)
        button_exit.grid(column = 0,row = 5)

        fig = Figure(figsize=(15, 8))
        ax = fig.add_subplot(111)
        line, = ax.plot(x, m)
        ax.grid()

        canvas = FigureCanvasTkAgg(fig, master= frame1)
        canvas.draw()
        canvas.get_tk_widget().grid(column = 1, row = 1)


    def updateOptions(self):
        simulation.blood = self._blood.get()
        simulation.wound = self._wound.get()
        simulation.sound = self._sound.get()
        del self._blood
        del self._wound
        del self._sound

    # Simulation SetupWindow
    def __DrawWindow3(self):
        #TODO: change to state 8 once server issues are resolved
        button_scenario =  Button(self._frame, text="Begin", command= lambda: [self._destroy_UpdateState(4)], font=("Arial", largetitletext), bg="firebrick3", fg="white", state='disabled')

        def updateScenarioButtonState():
            button_scenario['state'] = 'normal' if self._wound and self._blood and self._sound else 'disabled'

        def onConditionChange(*args):
            updateScenarioButtonState()

        # Attach the onConditionChange function to the traces
        self._wound.trace_add('write', onConditionChange)
        self._sound.trace_add('write', onConditionChange)
        self._blood.trace_add('write', onConditionChange)


        #Add Title frame
        framet = LabelFrame(self._frame,fg="black", bg="gray75")
        framet.place(x=.025*w, y=.025*h, height=.2*h, width=.95*w)    
        # Add a label at the top of the window
        label_scenario = Label(framet, text="Choose Scenario", font=("Arial", largetitletext), fg="black", bg="gray75", pady = 15)
        label_scenario.pack(fill = X)

        #Add the Frames
        #Add left frame
        frameL = LabelFrame(self._frame,bg="firebrick3", fg="white")
        frameL.place(x=.015*w, y=.25*h, height=.675*h, width=.3*w)    
        #Add Middle frame
        frameM = LabelFrame(self._frame, padx=50, pady=5,bg="firebrick3", fg="white")
        frameM.place(x=.345*w, y=.25*h, height=.325*h, width=.3*w)            
        #Add Right Frame
        frameR = LabelFrame(self._frame, padx=50, pady=5,bg="firebrick3", fg="white")
        frameR.place(x=.675*w, y=.25*h, height=.675*h, width=.3*w)

        # Add the left section with wound choice checkboxes
        label_wound_choice = Label(frameL, text="Mode:", bg="firebrick3", fg="white",font=("Arial", largetitletext), padx= 40)
        label_wound_choice.grid(row=0, column=0, pady=0)

        # Add the checkboxes for wound choice
        #wound = 1  #1=upper and 2=lower  
        checkbox_junction = Radiobutton(frameL, text="Packing",font=("Arial", smalltitletext), variable = self._wound,
                                        value=1,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=65, indicatoron=0,bd=10)

        checkbox_junction.grid(row=1, column=0,padx=40, pady=20)
        checkbox_armT = Radiobutton(frameL, text="Tourniquet",font=("Arial", smalltitletext), variable = self._wound,
                                    value=2,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=11, indicatoron=0,bd=10)

        checkbox_armT.grid(row=2, column=0,padx=40,pady=20)
        checkbox_armDP = Radiobutton(frameL, text="Pressure",font=("Arial", smalltitletext), variable = self._wound,
                                     value=3,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=45, indicatoron=0,bd=10)
        checkbox_armDP.grid(row=3, column=0,padx=40,pady=20)

         # Add the middle section with sound toggle switch
        label_sound = Label(frameM, text="Sound:", font=("Arial", largetitletext),bg="firebrick3", fg="white")
        label_sound.grid(row=0, column=0,columnspan=2, pady=0)    
        # Add the sound toggle switch
        #sound = 2
        checkbox_on = Radiobutton(frameM, text="On",font=("Arial", mediumtitletext), variable=self._sound,
                                  value=1,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=10, indicatoron=0,bd=10,)
        checkbox_on.grid(row=1, column=0,padx=0, pady=0)
        checkbox_off = Radiobutton(frameM, text="Off",font=("Arial", mediumtitletext), variable=self._sound,
                                   value=2,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=5, indicatoron=0,bd=10)
        checkbox_off.grid(row=1, column=1,padx=0,  pady=0)

        #Button to enter scenario in middle frame
        # TODO: change to state 8
        button_scenario = Button(self._frame, text="Begin", command= lambda: [self.updateOptions(), self._destroy_UpdateState(4)], font=("Arial", largetitletext), bg="firebrick3", fg="white", state='disabled')
        button_scenario.place(x=.345*w, y=.6*h, height=.15*h, width=.3*w)

        button_quit = Button(self._frame, text="Home", command = lambda: [self._destroy_UpdateState(1)],  font=("Arial", largetitletext),bg="firebrick3",fg="white")
        button_quit.place(x=.345*w, y=.775*h, height=.15*h, width=.3*w)

        # Add the right section with bleed out time checkboxes
        label_bleed = Label(frameR, text="Blood:", font=("Arial", largetitletext),bg="firebrick3", fg="white")
        label_bleed.grid(row=0, column=0, pady=0)
        # Add the checkboxes for bleed out time
        #blood = 3
        checkbox_high = Radiobutton(frameR, text="High",font=("Arial", mediumtitletext), variable=self._blood,
                                    value=1,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=110, indicatoron=0,bd=10)
        checkbox_high.grid(row=1, column=0,padx=0, pady=10)
        checkbox_low = Radiobutton(frameR, text="Low",font=("Arial", mediumtitletext), variable=self._blood,
                                   value=2,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=125, indicatoron=0,bd=10)
        checkbox_low.grid(row=2, column=0,padx=0,  pady=10)
        checkbox_off = Radiobutton(frameR, text="Off",font=("Arial", mediumtitletext), variable=self._blood,
                                   value=3,bg="firebrick4", fg="white", selectcolor="firebrick3",padx=150, indicatoron=0,bd=10)
        checkbox_off.grid(row=3, column=0,padx=0,  pady=10)


            
    # Simulation Window
    def __DrawWindow4(self):
        bleedoutbarframe = LabelFrame(self._frame,bg="firebrick3", fg="white")
        bleedoutbarframe.grid(row=0, column=0)
        graphframe = LabelFrame(self._frame,bg="firebrick3", fg="white")
        graphframe.grid(row=0, column=1)
       
        # Add the frame that the bleedout bar will go in
        label_bleedoutbar = Label(bleedoutbarframe, text="Blood\nLost", bg="firebrick3", fg="white", font=("Arial", mediumtitletext), padx=70, pady=10)
        label_bleedoutbar.grid(row=0, column=0,columnspan=2, sticky="w")
        axis_bleedoutbar = Label(bleedoutbarframe, text='-    3.0\n\n-    2.5\n\n-    2.0\n\n-    1.5\n\n-    1.0\n\n-    0.5\n\n- 0.0 (L)', font=('Arial', 35), fg="white", bg="firebrick3")
        axis_bleedoutbar.grid(row=1, column = 1)
        progbar = ttk.Progressbar(bleedoutbarframe,length=750, orient="vertical", mode="determinate",takefocus=True, maximum=3)      
        progbar.grid(row=1, column=0, ipadx=130)
        progbar['value'] = 0


        plt.rcParams.update({'font.size':22})
        fig = Figure(figsize=(15, 10.1))        
           
        ax = fig.add_subplot(111)
        ax.set_title('Pressure', fontsize=80)
        ax.set_xlabel('Time (s)', fontsize=40)
        ax.set_ylabel('Pressure at Bleed (LBS)', fontsize=40)
        ax.set_xlim(-20, 20)
        ax.set_ylim(0, 30)
        line, = ax.plot(simulation.timelist, simulation.pressurelist, label='Your Pressure', linewidth=5, color = 'b')
        line_20ref, = ax.plot(simulation.timelist, simulation.ma_xlist, label='Target Pressure', linewidth=5, color = 'r' )
        ax.legend(loc='upper left', fontsize=20)
       
        # Add the canvas for the graph
        canvas_graph = FigureCanvasTkAgg(fig, master=graphframe)  # A tk.DrawingArea.
        canvas_graph.draw()
        canvas_graph.get_tk_widget().grid(row=1,column=0)

       
        # TODO: Possible speedup from combining events need to find way to pass multiple values in event
        def Update_Sim_Window(event1):
            big_BloodLost1 = float(event1.state)
            BloodLost1 = big_BloodLost1 / 1000000    
            simulation.blood_loss.append(BloodLost1)
            progbar['value'] = BloodLost1
           
        def Update_pressure(event2):
            big_pressure = float(event2.state)
            smallpressure = big_pressure / 1000000    
            simulation.pressurelist.append(smallpressure)

           
        def Update_time(event3):
            big_time = float(event3.state)
            smalltime = big_time / 1000000    
            simulation.timelist.append(smalltime)
            simulation.ma_xlist.append(20)
            ax.set_xlim(smalltime - 30, smalltime + 10)  # Adjust the axis limits based on your data
            line, = ax.plot(simulation.timelist, simulation.pressurelist, label='Your Pressure', linewidth=5, color = 'b')
            line_20ref, = ax.plot(simulation.timelist, simulation.ma_xlist, label='Target Pressure', linewidth=5, color = 'r' )
            canvas_graph.draw()

        self._root.bind("<<event1>>",Update_Sim_Window)
        self._root.bind("<<event2>>",Update_pressure)
        self._root.bind("<<event3>>",Update_time)




    # Failed Simulation Window
    def __drawWindow5(self):
        #Add Title 
        frame1 = LabelFrame(self._frame, pady=25, fg="black", bg="gray75")
        frame1.place(x=.025*w, y=.025*h, height=.2*h, width=.95*w)
        # Add a label at the top of the window
        label_home = Label(frame1, text="You Failed", font=("Arial", largetitletext), fg="black", bg="gray75")
        label_home.pack(fill = X)
        # Add two buttons underneath the label of home page

        button_scenario = Button(self._frame, text="View\nGraph", command = lambda: [self._destory_UpdateState(7)], bg="firebrick3",fg="white",  font=("Arial", largetitletext), padx=10, pady=200)
        button_scenario.place(x=.025*w, y=.25*h, height=.675*h, width=.47*w)
        button_retrieve = Button(self._frame, text="Select\nNew User", command = lambda: [self._destory_UpdateState(8)], bg="firebrick3",fg="white", font=("Arial", largetitletext), padx=10, pady=200)
        button_retrieve.place(x=.5025*w, y=.25*h, height=.675*h, width=.47*w)


    # Successful Simulation Window
    def __DrawWindow6(self):
        #Add Title frame        
        frame1 = LabelFrame(self._frame, pady=25, fg="black", bg="gray75")
        frame1.place(x=.025*w, y=.025*h, height=.2*h, width=.95*w)
        # Add a label at the top of the window
        label_home = Label(frame1, text="You Stopped The Bleed", font=("Arial", largetitletext), fg="black", bg="gray75")
        label_home.pack(fill = X)
        # Add two buttons underneath the label of home page

        button_scenario = Button(self._frame, text="View\nGraph", command = lambda: [self._destroy_UpdateState(7)], bg="firebrick3", fg="white", font=("Arial", largetitletext), padx=10, pady=200)
        button_scenario.place(x=.025*w, y=.25*h, height=.675*h, width=.47*w)
        button_retrieve = Button(self._frame, text="Select\nNew User", command = lambda: [self._destroy_UpdateState(8)], bg="firebrick3",fg="white", font=("Arial", largetitletext), padx=10, pady=200)
        button_retrieve.place(x=.5025*w, y=.25*h, height=.675*h, width=.47*w)


    # Completed Simulation Graph Window
    def __DrawWindow7(self):
        button_home = Button(self._frame, text="Select\nNew User", command = lambda: [self._destroy_UpdateState(8)], bg="firebrick3",fg="white", font=("Arial", largetext))
        button_home.place(x=0, y=.4*h, height=.2*h, width=.125*w)
        #Create graph frame
        frame2 = Frame(self._frame, pady=25, bg="gray75")
        frame2.place(x=.125*w, y=0, height=h, width=.85*w)
       
        #Add the frame that the graph will go in
        plt.rcParams.update({'font.size':22})
        fig = Figure(figsize=(18, 10.1))        
           
        ax = fig.add_subplot(111)
        ax.set_title('Simulation Summary', fontsize=80)
        ax.set_xlabel('Time (s)', fontsize=40)
        ax.set_ylabel('Pressure at Bleed (LBS)', fontsize=40)
        ax.set_xlim(0, max(simulation.timelist) + 5)  # Adjust the axis limits based on your data
        ax.set_ylim(0, max(simulation.pressurelist) +5)
        line, = ax.plot(simulation.timelist, simulation.pressurelist, label='Your Pressure', linewidth=5, color = 'b')
        line_20ref, = ax.plot(simulation.timelist, simulation.ma_xlist, label='Target Pressure', linewidth=5, color = 'r' )
        ax.legend(loc='upper left', fontsize=20)


    # Class Window
    def __DrawWindow8(self):
        # Function to enable/disable the "Start" button based on whether a user is selected

        def update_button_states():
            selected_index = user_listbox.curselection()
            if selected_index:
                network.User = network.Class.users[selected_index[0]]
                button_start['state'] = 'normal'
                button_view_graph['state'] = 'normal' if network.User.training_data['x_list'] else 'disabled'
            else:
                button_start['state'] = 'disabled'
                button_view_graph['state'] = 'disabled'

        # Button to start simulation if a student is selected
        def start_simulation():
            selected_index = user_listbox.curselection()
            if selected_index:
                # Change state to simulation
                self._destroy_UpdateState(4)

        def request():
            network.make_http_get_request(input_entry.get())
            populate_listbox()

        # Function to populate the Listbox with users from the current class
        def populate_listbox():
            user_listbox.delete(0, END)  # Clear the listbox
            if network.Class:
                for user in network.Class.users:
                    has_training_data = bool(user.training_data['x_list'])
                    status = "Complete" if has_training_data else "Incomplete"
                    display_name = f"{status} - {user.name}"
                    user_listbox.insert(END, (display_name))


        # Button to run a function using the selected user's ID
        def view_graph():
            selected_index = user_listbox.curselection()
            if selected_index:
                global timelist, pressurelist, ma_xlist
                timelist = (network.Class.users[selected_index[0]].training_data['x_list'])
                pressurelist = (network.Class.users[selected_index[0]].training_data['y_list'])
                ma_xlist = (network.Class.users[selected_index[0]].training_data['ma_xlist'])
                self._destroy_UpdateState(7)

        #Add Title frame
        framet = LabelFrame(self._frame,fg="black", bg="gray75")
        framet.place(x=.025*w, y=.025*h, height=.2*h, width=.95*w)    
        # Add a label at the top of the window
        label_scenario = Label(framet, text="Connect to Class", font=("Arial", largetitletext), fg="black", bg="gray75", pady = 15)
        label_scenario.pack(fill = X)

        # Add left frame
        frameL = LabelFrame(self._frame, bg="firebrick3", fg="white")
        frameL.place(x=.015 * w, y=.25 * h, height=.675 * h, width=.3 * w)

        label_input_field = Label(frameL, text="Class Key:", bg="firebrick3", fg="white", font=("Arial", smalltitletext), padx=40)
        label_input_field.grid(row=0, column=0, pady=0)

        # Add the entry for training key
        input_entry = Entry(frameL, font=("Arial", mediumtext), bg="firebrick4", fg="white", bd=10)
        input_entry.grid(row=1, column=0, padx=40, pady=20)

        # Button to make HTTP Request (or perform desired action)
        button_make_request = Button(frameL, text="Connect", font=("Arial", smalltitletext), bg="firebrick4", fg="white", command=lambda: request())
        button_make_request.grid(row=2, column=0, padx=40, pady=20)# Button to go back to the home window

        button_start = Button(self._frame, text="Start", command=start_simulation, font=("Arial", largetext), bg="firebrick3", fg="white", state='disabled')
        button_start.place(x=.345*w, y=.325*h, height=.15*h, width=.3*w)
       
        button_back = Button(self._frame, text="Go Back", command= lambda: [self._destroy_UpdateState(3)], bg="firebrick3", fg="white", font=("Arial", largetext))
        button_back.place(x=.345*w, y=.5*h, height=.15*h, width=.3*w)

        # Button to go back to the home window
        button_home = Button(self._frame, text="Home", command= lambda: [self._destroy_UpdateState(1)], bg="firebrick3", fg="white", font=("Arial", largetext))
        button_home.place(x=.345*w, y=.675*h, height=.15*h, width=.3*w)


        # Scrollable Listbox to display users
        user_listbox = Listbox(self._frame, selectmode=SINGLE, font=("Arial", mediumtext), bg="firebrick4", fg="white", bd=10)
        user_listbox.place(x=.675*w, y=.25*h, height=.5*h, width=.3*w)
       
        # Bind the function to the Listbox selection event
        user_listbox.bind('<<ListboxSelect>>', lambda event: update_button_states())

        button_view_graph = Button(self._frame, text="View Graph", command=view_graph, font=("Arial", largetext), bg="firebrick3", fg="white", state='disabled')
        button_view_graph.place(x=.675 * w, y=.775 * h, height=.15*h, width=.3*w)
       
        populate_listbox()

    def handleQueue(self):
        while simulation.P:
            data = simulation.eventQueue.get()
            self._root.event_generate("<<event2>>", state=str(data[1]))
            self._root.event_generate("<<event3>>", state=str(data[2]))
            self._root.event_generate("<<event1>>", state=str(data[0]))


