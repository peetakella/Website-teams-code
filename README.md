# Better Bleeding Control
The better bleeding control is a medical training device designed to hyper realistically simultate human bloodflow to train medical students how to properly stop the bleed.
All intellectual property is owned by the Texas Tech University chapter of chapter of Stop the Bleed.

## Updating the README
The README should be updated as frequently as possible to ensure effective comminictaion among the members working on the device and its outside components, and allow for easy onboarding of new members.
The main function of the README will be a highlevel overview of the system as a whole, and goals currently being pursued lastly a section exploring future considerations for improvement.

## System Overview
The System currently opperates in a single python file. The decision to use a python file was made primarly due to its ease of entry for non-programmers. Going forward files should be written smaller and with small attainable goals.

### Dependencies
- **Tkinter**: This python library shall be used as the primary driver for the graphical user interface
- **Time**: This library shall be used to track the flow of seconds durring a simulation.
- **Matplotlib**: This libarary shall be used to create the graphs that display data obtrained throughout a simulation.
- **Numpy**, **Math**: These libraries will be used to make mathematical calculations to translate data into meaningful user data.
- **Pygame**: This library shall be used for the audio output as it is a much crisper audio than the the audio features provided by the other libraries.
- **Requests**, **Json**, **Pexpect**: These libraries shall be used for communication witht the companion website that is used by students and trainers.
- **Threading**: This library is used to have a single thread for the GUI and a Thread for the data collection. There may be an optimization to have these run on a single thread.
- **Smbus**: This library shall be used for communication with the sensors.
- **Rpi.GPIO**: This library shall be used for control of the input, output pins in the microcontroller.

These Dependencies currently have some redundant imports that may be fixed in order to improve intial load speeds.

### Global Variables and Classes
- **Global Variables**
    1) Address to the Website
    2) Various List for data collected during a simulation.
    3) A variable that stores the current class being taught.
    4) Various Variables to standardize GUI elements.
    5) Various variables for audio control
- **Classes**
    1) User: This class stores variables for users (primarily students) that will be running the simulation.
    2) TrainingClass: This class stores the authorized users in the class being taught and it's own ID.

### Functions
- 10 Functions that Define and Draw and close the GUI window.
- 3 Debugging Functions that write to STDIO the data that has been collected.
- 2 Functions for HTTP Communication with the companion website.
- 1 Background function that controls electrical signals collects data and performs every function not being performed above.
- 1 Function to shutoff the motor.

## Goals
The following is a list of the goals that the project has been funded to achieve:
1) **New Motor Integration**: A Quiter motor that uses a new software than the one currently being used.
2) **Sound Algorithm**: Improving the sound algorithm to more closely mimic a human in tremendous pain.
3) **Website Integration and Design**: Cleaning up the look and feel and optimizing to make the project more professional.
4) **Improve the rate of Sampling of the code from the sensors**: Currently the sampling rate is slowing down the GUI graph rendering tremendously.
5) **Graphic User Interface Design**: The current GUI is outdated and does notlook or feel good to use.


## Future Considerations
1) **Refactoring**: The codebase does not follow best practices for good Software Design.
2) **Docker**: As the project has many dependencies it may be worth considering using Docker to create image files that allow for automatic integration of these dependencies.
