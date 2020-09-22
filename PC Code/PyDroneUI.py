# Aquatic Surface Drone UI

import wx
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as plticker
import subprocess
from shutil import copyfile
from sys import exit
from datetime import datetime

class DroneMenu(wx.Frame):
    global sourcePath
    global fileName
    global pingFound
    sourcePath = "empty"
    
    def __init__(self, *args, **kw): 
        super(DroneMenu, self).__init__(*args, **kw)

        self.InitUI()
    
    def InitUI(self):
        panel = wx.Panel(self)
    
        self.text1 = wx.StaticText(panel, label = "Finding Drone", 
                                   pos = (320, 10))
        
        self.text2 = wx.StaticText(panel, label = "", pos = (210, 230))
        
        self.text3 = wx.StaticText(panel, label = "", pos = (470, 230))
        
        Button = wx.Button(panel,wx.BU_TOP, label = 'Open', pos = (210,200))
        Button.Bind(wx.EVT_BUTTON, self.OnOpen)
        
        Button2 = wx.Button(panel, label = 'Save', pos = (470,200))
        Button2.Bind(wx.EVT_BUTTON, self.OnSaveAs)
        
        Button3 = wx.Button(panel, label = 'Graph', pos = (340,200))
        Button3.Bind(wx.EVT_BUTTON, self.Graph)
        
        font = wx.Font(13, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, 
                       wx.FONTWEIGHT_BOLD)
        self.text1.SetFont(font)
        self.SetBackgroundColour('NAVY')
        self.text1.SetForegroundColour('WHITE')
        self.text2.SetForegroundColour('WHITE')
        self.text3.SetForegroundColour('WHITE')
        self.SetSize((790, 300)) 
        self.SetTitle('Aquatic Surface Drone')
        self.Centre()
        png = wx.Image("FIU1.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bitmap = wx.StaticBitmap(self, -1, png, (340, 50), 
                                      (png.GetWidth(), png.GetHeight()))
        if(pingDrone()):
            self.text1.SetLabel("Drone Connected!")
        else:
            self.text1.SetLabel("Drone not connected!")
              
    def OnOpen(self, event): 
        if(not pingFound):
            self.text2.SetLabel("Drone not found")
            return
        self.text3.SetLabel("")
        dataDir = "\\\\ApexDrone\\pi\\Data\\"
        openFile = wx.FileDialog(self, message = "Select CSV file", 
                defaultDir = dataDir,
                wildcard="CSV files (*.csv)|*.csv", 
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFile.SetDirectory(dataDir)
        with openFile as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind
            # Proceed loading the file chosen by the user
            global fileName
            global sourcePath
            sourcePath = fileDialog.GetPath()
            fileName = os.path.basename(sourcePath)
            self.text2.SetLabel(fileName)

    def OnSaveAs(self, event):    
        if(sourcePath == "empty"):
            self.text3.SetLabel("Please select a file!")
            return
        saveFile = wx.DirDialog (None, "Choose where to save", "C:\\",
                    wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        
        with saveFile as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # save the current contents in the file
            global fileName
            targetPath = fileDialog.GetPath() + "\\" + fileName
            
            try:
                copyfile(sourcePath, targetPath)
                self.text3.SetLabel("Saved!")
            except IOError as e:
                print("Unable to copy file. %s" % e)
                exit(1)
            
    def Graph(self, event):
        if(not sourcePath == 'empty'):
            self.SetSize((790, 880))
            computeMission()
            # Create Conductivity png
            png = wx.Image("conductivity.png", 
                           wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.bitmap = wx.StaticBitmap(self, -1, png, (20, 270), 
                                      (png.GetWidth(), png.GetHeight()))
            # Create Temperature png
            png = wx.Image("temperature.png", 
                           wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.bitmap = wx.StaticBitmap(self, -1, png, (400, 270), 
                                      (png.GetWidth(), png.GetHeight()))
            # Create pH png
            png = wx.Image("pH.png", 
                           wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.bitmap = wx.StaticBitmap(self, -1, png, (20, 540), 
                                      (png.GetWidth(), png.GetHeight()))
            
            # Create Salinity png
            png = wx.Image("salinity.png", 
                           wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.bitmap = wx.StaticBitmap(self, -1, png, (400, 540), 
                                      (png.GetWidth(), png.GetHeight()))
        return

def computeMission():
    # Get data from csv to panda DataFrame
    missionData = pd.read_csv(sourcePath)
    timeData = missionData[["Time"]]
    latData = missionData[["Latitude"]]
    longData = missionData[["Longitude"]]
    conductivityData = missionData[["Conductivity"]]
    temperatureData = missionData[["Temperature"]]
    pHData = missionData[["pH"]]
    salinityData = missionData[["Salinity"]]
    
    
    missionData.Time = missionData.Time.map(lambda x: datetime.strptime(x,
                        "%Y-%m-%d %H:%M:%S"))

    # Conductivity Graph
    graphTitle = ('Conductivity Over Time')
    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    myFmt = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(myFmt)
    
    # Tweak spacing to prevent clipping of tick-labels 
    plt.subplots_adjust(bottom = 0.2) 
    plt.margins(0.02)
    # this locator puts ticks at regular intervals
    loc = plticker.MultipleLocator(base=.001) 
    ax.xaxis.set_major_locator(loc)
    
    ax.set_title(graphTitle)
    ax.set_ylabel('µS/cm')
    ax.set_xlabel('time (HH:MM:SS)')
    ax.plot(missionData.Time, conductivityData)
    fig.savefig('conductivity', dpi=58)
    
    # Temperature Graph
    graphTitle = ('Temperature Over Time')
    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    ax.xaxis.set_major_formatter(myFmt)
    
    plt.subplots_adjust(bottom = 0.2) 
    plt.margins(0.02)
    loc = plticker.MultipleLocator(base=.001) 
    ax.xaxis.set_major_locator(loc)
    
    ax.set_title(graphTitle)
    ax.set_ylabel('Fahrenheit')
    ax.set_xlabel('time (HH:MM:SS)')
    ax.plot(missionData.Time, temperatureData)
    fig.savefig('temperature', dpi=58)
    
    # pH Graph
    graphTitle = ('pH Over Time')
    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    ax.xaxis.set_major_formatter(myFmt)
  
    plt.subplots_adjust(bottom = 0.2) 
    plt.margins(0.02)
    loc = plticker.MultipleLocator(base=.001) 
    ax.xaxis.set_major_locator(loc)
    
    ax.set_title(graphTitle)
    ax.set_ylabel('pH')
    ax.set_xlabel('time (HH:MM:SS)')
    ax.plot(missionData.Time,  pHData)
    fig.savefig('pH', dpi=58)
    
    # Salinity Graph
    graphTitle = ('Salinity Over Time')
    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    ax.xaxis.set_major_formatter(myFmt)
  
    plt.subplots_adjust(bottom = 0.2) 
    plt.margins(0.02)
    loc = plticker.MultipleLocator(base=.001) 
    ax.xaxis.set_major_locator(loc)
    
    ax.set_title(graphTitle)
    ax.set_ylabel('ppm')
    ax.set_xlabel('time (HH:MM:SS)')
    ax.plot(missionData.Time,  salinityData)
    fig.savefig('salinity', dpi=58)
    
    return
       
def pingDrone():
    global pingFound
    response = subprocess.call(['ping', '-n', '1', "ApexDrone"]) 
    if response == 0:
        pingFound = True
        return True
    else:
        pingFound = False
        return False
        
        
def main(): 
    app = wx.App() 
    menu = DroneMenu(None) 
    menu.Show() 
    app.MainLoop()
     
  
if __name__ == '__main__': 
    main()  