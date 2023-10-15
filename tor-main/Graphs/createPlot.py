import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime   
from sys import argv
from subprocess import call
import os.path


#plt.plot([1,2,3])
#plt.show()
def createPlot(uniqueTor):
    #check if file exists
    if (os.path.exists(uniqueTor) == False):
        print("This data hasn't been found yet.")
        i = input("Would you like to find it now? Y/N ")
        if (i == 'y' or i == 'Y'):
            call(["./downloadData", str(startMonth), str(startYear), str(endMonth), str(endYear)])
            call(["./findData", str(startMonth), str(startYear), str(endMonth), str(endYear)])
        
    #Gathering data from file    
    print("Creating graph now.")
    f = np.genfromtxt(uniqueTor, str)
    date = []
    uniqueTor = []
    torAS = []
    for i in f:
        date.append(datetime.strptime(i[0], '%m-%d-%Y')) #11-01-2007
        uniqueTor.append(int(i[1]))
        torAS.append(int(i[2]))

    #x = np.genfromtxt("uniqueAS-200711-20218.txt", str)

    #dateAS = []
    #uniqueAS = []
    #for i in x:
        #dateAS.append(datetime.strptime(i[0], '%m-%d-%Y')) #11-01-2007
        #uniqueAS.append(int(i[1]))

    plt.plot(date, uniqueTor, label="Unique Tor IPs")
    plt.plot(date, torAS, label = "Unique Tor ASes")
    #plt.plot(dateAS, uniqueAS, label = "Unique ASes")
    plt.legend()
    #plt.set(xlabel='time')
    #plt.show()
    imageName = "uniqueIPAS_image-%s%s-%s%s.png" %(startYear, formattedStartMonth, endYear, formattedEndMonth)
    plt.savefig(imageName)

def main():
    startMonth = argv[1]
    startYear = argv[2]
    endMonth = argv[3]
    endYear = argv[4]

    formattedStartMonth = startMonth.zfill(2)
    formattedEndMonth = endMonth.zfill(2)

    uniqueTor = "results-%s%s-%s%s.txt" %(startYear, formattedStartMonth, endYear, formattedEndMonth)
