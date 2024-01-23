import matplotlib.pyplot as plt #graphing
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Fonts and texts
largetitletext = 105
mediumtitletext = 80
smalltitletext = 70
largetext=55
mediumtext = 30
smalltext = 25
x=3

root = Tk()
root.title("Better Bleeding Control")
##print ('main thread', threading.get_ident())
root.configure(bg="grey75")
#w = 1920
w=1920
h = 1080
root.geometry("{}x{}".format(w, h))
# Add Title frame
frame = Frame(root)
frame.pack(expand=True, fill=BOTH)



if x==1:
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
    button_retrieve = Button(frame, text="Select\nNew User", command = lambda: [open_class_window()],bg="firebrick3",fg="white", font=("Arial", largetitletext), padx=10, pady=200)
    button_retrieve.place(x=.5025*w, y=.25*h, height=.675*h, width=.47*w)
elif x == 2:
    print('if window = 5')
    #Add Title frame        
    frame1 = LabelFrame(frame, pady=25, fg="black", bg="gray75")
    frame1.place(x=.025*w, y=.025*h, height=.2*h, width=.95*w)
    # Add a label at the top of the window
    label_home = Label(frame1, text="You Failed", font=("Arial", largetitletext), fg="black", bg="gray75")
    label_home.pack(fill = X)
    # Add two buttons underneath the label of home page
elif x == 3:
    button_scenario = Button(frame, text="View\nGraph", command = lambda: [View_Graph()], bg="firebrick3",fg="white",  font=("Arial", largetitletext), padx=10, pady=200)
    button_scenario.place(x=.025*w, y=.25*h, height=.675*h, width=.47*w)
    button_retrieve = Button(frame, text="Select\nNew User", command = lambda: [open_class_window()],bg="firebrick3",fg="white", font=("Arial", largetitletext), padx=10, pady=200)
    button_retrieve.place(x=.5025*w, y=.25*h, height=.675*h, width=.47*w)

    print('if window = 7')
    ##print ('wound', wound)
    ##print ('Sound', sound)
    ##print ('blood', blood)      
    #Add Title frame        
    button_home = Button(frame, text="Select\nNew \nUser", command = lambda: [open_class_window()],bg="firebrick3",fg="white", font=("Arial", largetext))
    button_home.place(x=0, y=.35*h, height=.3*h, width=.125*w)
    #Create graph frame
    frame2 = Frame(frame, pady=25, bg="gray75")#.pack(fill=BOTH, expand = True)
    frame2.place(x=.125*w, y=0, height=.95*h, width=.875*w)
    # Add a label at the top of the window
    #label_home = Label(frame1, text="Simulation Summary", font=("Arial", largetitletext), fg="black", bg="gray75")
    #label_home.pack(fill = X)
   
    #Add the frame that the graph will go in
    plt.rcParams.update({'font.size':22})
    fig = Figure(figsize=(18, 10.1))        
    '''time = [0,1,2,3,4,5,6,7,8,9,10]
    pressure = [2,3,4,3,4,5,4,6,5,5,18]
    ma_x = [20,20,20,20,20,20,20,20,20,20,20]'''
       
    ax = fig.add_subplot(111)
    ax.set_title('Simulation Summary', fontsize=80)
    ax.set_xlabel('Time (s)', fontsize=40)
    ax.set_ylabel('Pressure at Bleed (LBS)', fontsize=40)
    '''ax.set_xlim(0, max(timelist) + 5)  # Adjust the axis limits based on your data
    ax.set_ylim(0, max(pressurelist) +5)
    line, = ax.plot(timelist, pressurelist, label='Your Pressure', linewidth=5, color = 'b')
    line_20ref, = ax.plot(timelist, ma_xlist, label='Target Pressure', linewidth=5, color = 'r' )
    ax.legend(loc='upper left', fontsize=20)'''
   
    # Add the canvas for the graph
    canvas_graph = FigureCanvasTkAgg(fig, master=frame2)  # A tk.DrawingArea.
    canvas_graph.draw()
    canvas_graph.get_tk_widget().pack(fill=BOTH, expand = True) 
