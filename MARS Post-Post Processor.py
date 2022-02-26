from datetime import datetime
from distutils.log import info
import os
import glob
from pickle import FALSE
import tkinter as tk

version = "1.2"

root = tk.Tk()
root.title("M.A.R.S. Post-Post Processor- v"+version)
windWidth = 350
windHeight = 150
canvas1 = tk.Canvas(root, width = windWidth, height = windHeight)

canvas1.pack()

exePath = os.getcwd()
inFolder = exePath + '\In\\'
outFolder = exePath + '\Out\\'

# Check for in and out folder, create if they don't exist
if os.path.exists(inFolder) == False:
    os.mkdir(inFolder)
if os.path.isdir(outFolder) == False:
    os.mkdir(outFolder)


def ProcessFiles():
    print("----------------------------")
    print("----------------------------")
    
    #Get current date/time
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%y %H:%M:%S")

    # Get list of files in the IN folder
    cncFiles = glob.glob(inFolder + '*.txt')
    
    # Loop through all files in 'IN' folder
    for cncFile in cncFiles:
        # Read all lines from processing file
        file = open(cncFile, "r")
        lines = file.readlines()
        file.close

        # Define found code variables
        spindleOn = False #Only stop for spindle at start of program
        unitsAreMetric = True #Don't tell machine to go to -10in z postion. that would be bad
        
        # Create new file name, same as IN, but '.nc' type
        newFileName = os.path.splitext(os.path.basename(cncFile))[0]
        newFile = newFileName + '.nc'

        # Open new file for write
        file = open(outFolder + newFile, "w")
        file.writelines("(Processed by M.A.R.S. " + dt_string + ")\n")
        lastLine = ""

        #loop through all lines to write new file
        for line in lines:
            line = line.strip().upper()
            #print(line)
            
            # If current line contains 'G20' set metric units to false
            if line.find("G20")!=-1:
                # 'G20' specifies imperial unints, 'G21' specifies metric
                unitsAreMetric = False

            # If current line contains 'M30' write text before
            if line.find("M30") != -1:
                # M30 is the end of program command
                # Turn off spindle
                file.writelines("M05\n")
                # Go to back of machine
                if unitsAreMetric:
                    file.writelines("G53 Z-11.\n")
                    file.writelines("G53 Y-11.\n")
                else:
                    file.writelines("G53 Z-0.6\n")
                    file.writelines("G53 Y-0.6\n")
                # End if metric
            # End find 'M30'

            # If current line does not contain 'G28' write line
            if line.find("G28") == -1 & line.find("(THIS POST") == -1 & line.find("(WITHOUT") == -1:
                file.writelines(line + "\n")
                #print(line)
            
            # If current line contains 'M03' write text after            
            if line.find("M03") != -1:
                # M03 is a spindle on command
                if  spindleOn!=True:
                    spindleOn = True
                    file.writelines("M00\n")
                    file.writelines("(--------------------------------)\n")
                    file.writelines("(MAKE SURE THE SPINDLE IS RUNNING)\n")
                    file.writelines("(     THEN PRESS CYCLE START     )\n")
                    file.writelines("(--------------------------------)\n")
                # End if SpindleON!True
            # End if Find M03
            lastLine = line
        # End lines loop

        # Close new file
        file.close()

        # Delete old file
        os.remove(cncFile)
        if os.path.exists(inFolder + newFileName + ".set"):
            os.remove(inFolder + newFileName + ".set")
        
    # End files loop

    # Tell user files were converted
    lblTxt = 'Converted ' + str(len(cncFiles)) + ' file(s)\n' + dt_string
    label1 = tk.Label(root, text= lblTxt, fg='green', font=('helvetica', 12, 'bold'))
    canvas1.create_window(windWidth/2, 110, window=label1)

# Create Label
label2 = tk.Label(root,text = exePath)
canvas1.create_window(windWidth/2,10, window=label2)
# Create button
button1 = tk.Button(text='Process Files',command=ProcessFiles, bg='brown',fg='white', font=('helvetica',22,'bold'))
canvas1.create_window(windWidth/2, 50, window=button1)

# Show GUI window
root.mainloop()