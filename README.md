# Stop the Bleed
Stop the Bleed by Better Bleeding Control is a medical training simulator used to train individuals how to properly stop bleeding out.
The simulation has 3 modes:
    1) Wound Packing
    2) Tournequet
    3) Direct Pressure

This Repository is the main repository for managing the software that goes into the device and is the property of Better Bleeding Control.
The unauthorized replication or use of any of the assets in this repository will leave the violator subject to legal repurcussions from Better Bleeding Control.

This project is currently unlicensed, but will likely be puruing either a GLPL or another license of some sort.

## Installation and Usage
**Python 3.11 >" is required**
The Below Steps are used to install the software on a new rasberry pi:
1) Clone the Repository
2) Navigate into the repository
3) run `chmod u+x install.sh` if the file is not already an executable
4) run `sudo ./install.sh`
5) run `reboot` to begin using the application

In the future this section will include how to set up the hardware for the rasberry pi as well.

## Development Practices
As of 01/31/2024 the main branch is unprotected other than simply being in a private repository. This should be changed in the near future.

As development proceeds all changes should be made and pushed on a seperate branch.
Once branches are merged with the main branch they should be deleted from the online repository.

### Documentation
Any New programs written should include at the top a comment with the following:
1) Title of the program
2) Author(s) of the program
3) Description of what the program is trying to acheive
4) Version a complete refactor will increase the version of that file by 1 minor chnages will increase the version by 0.01

If there is only a minor change being made to the file then only comment the author at the section being updated.

### README.md
This README.md should be read and updated a minimum of once a week during a sprint and once a month in between development sprints.

### Sensor Errors
At the moment of wirting both of the packing sensors are not working.
If you run into sensors errors you can run `i2cdetect -y 1` and if all sensors are working you will see 0x26, 0x27, and 0x28
0x28 is the one that is used for packing.
On the old arm 0x27 is not working which tournequet, but for our testing we have swapped the pressure and tournequet address for this arm.
