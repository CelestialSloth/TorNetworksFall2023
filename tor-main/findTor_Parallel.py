#!/usr/bin/python3
import multiprocessing
import stem.descriptor.collector
from stem.descriptor import parse_file
from sys import argv
from multiprocessing import Pool
import os.path
import argparse

"""Collects the ip addr from every hours of the first day of the given year-month.

    Write all the tor IP addresses to file called findingUniqueTorIP-year-month.
    If a file doesn't exist, it is skipped.

    Args:
        month
        year
"""
def findTor(month: str, year: str, bandwidth):
    month = str(argv[1])
    year = str(argv[2])
    print("finding tor for", month, year)
    filename_start = "consensuses-%s-%s/01/%s-%s-01-" %(year, month, year, month)
    f = open("data/formatted/torIPLists/torIPList-%s-%s" %(year, month), "w")

    print("findTor.py: Going through each hour")
    for hour in range(1, 24):
        formattedHour = "0" + str(hour) if hour < 10 else str(hour)
        filename_end = "%s-00-00-consensus" %formattedHour
        filename = filename_start + filename_end
        if (bandwidth == True):
            for d in parse_file(filename): #TODO: IP list
                f.write("%s %i\n" %(d.address, d.bandwidth)) 
        else:
            for d in parse_file(filename): #TODO: IP list
                f.write(d.address + '\n') 
    f.close()

    return filename

def findTorParallel(month: str, year: str, bandwidth: bool):
    """
    Args:
        month:
        year:
        bandwidth: whether we should calculate bandwidth
    """
    #Create new file including info on year and month
    monthFormatted = month.zfill(2)
    print("Finding tor for", monthFormatted, year)
    f_filename = "data/formatted/torIPLists/torIPList-%s-%s" %(year, monthFormatted)
    f = open(f_filename, "w")

    #Generic beginning of the file the program is searching in
    filename_start = "consensuses-%s-%s/01/%s-%s-01-" %(year, monthFormatted, year, monthFormatted)
    
    #Looping through all hours in the day
    for hour in range(0, 24):
        formattedHour = "0" + str(hour) if hour < 10 else str(hour)
        filename_end = "%s-00-00-consensus" %formattedHour
        filename = filename_start + filename_end
        if (os.path.exists(filename) != True):
            print("File doesn't exist: ", filename)
        else:
            if (bandwidth == True):
                for d in parse_file(filename): #TODO: IP list
                    f.write("%s %i\n" %(d.address, d.bandwidth)) 
            else:
                for d in parse_file(filename): #TODO: IP list
                    f.write(d.address + '\n') 

    if os.stat(f_filename).st_size == 0: #If file is empty make sure it doesn't crash
        f.write("0")
    f.close()

#TODO: findTor_Parallel w/ bandwidth

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=int, required=True, nargs = 2)
    parser.add_argument('-e', type=int, default=None, nargs = 2)
    #TODO: fix -b option
    parser.add_argument('-b', type=bool, default=False, nargs = 1)
    args = parser.parse_args()  

    startMonth = args.s[0]
    startYear = args.s[1]
    endMonth = startMonth if args.e is None else args.e[0]
    endYear = startYear if args.e is None else args.e[1]
    bandwidth = args.b[0]
    print("Finding bandwidth: ", bandwidth)

    dates = []
    while ((startYear < endYear ) or (startMonth <= endMonth and startYear == endYear )):
        dates.append([str(startMonth), str(startYear), bandwidth])

        startMonth += 1
        if (startMonth == 13):
            startYear += 1
            startMonth = 1

    with Pool(processes=8) as pool:
        pool.starmap(findTorParallel, dates)
    return

if __name__ == '__main__':
    main()

