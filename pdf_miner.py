#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
the module extracts textual data of specific pattern from pdfs forming text files and then convert text files to csv table files,

"""
import subprocess
import io
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import re
import csv
#import sys, getopt
from cStringIO import StringIO

#-------------------------------------------------------------------------------------------
#function for creating a folder in directory
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
#--------------------------------------------------------------------------------------------
#function for converting single pdf to text file
def pdf_to_text(pdfname):
    # PDFMiner boilerplate
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Extract text
    fp = file(pdfname, 'rb')
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
    fp.close()
    # Get text from StringIO
    text = sio.getvalue()
    device.close()
    sio.close()
    return text
#------------------------------------------------------------------------------------------------------------
#function for converting multiple pdf to text files
def convertMultiple(pdfDir, txtDir):
    #if pdfDir == "": pdfDir = os.getcwd() + "\\" #if no pdfDir passed in
    for pdf in os.listdir(pdfDir): #iterate through pdfs in pdf directory
        fileExtension = pdf.split(".")[-1]
        if fileExtension == "pdf":
            pdfFilename = pdfDir + pdf
            text = pdf_to_text(pdfFilename) #get string of text content of pdf
            textFilename = txtDir + pdf.split(".")[0] + ".txt"
            textFile = open(textFilename, "w") #make text file
            textFile.write(text) #write text to text file
			#textFile.close

#create folder for storing text files
createFolder('./texts/')
#create folder for storing csv table files
#createFolder('./csvs/')

csvDir = "C:/Users/Hamad Nasir/Desktop/materials/"
pdfDir = "C:/Users/Hamad Nasir/Desktop/materials/pdfs/"
txtDir = "C:/Users/Hamad Nasir/Desktop/materials/texts/" #create texts folder in directory for simplicity
#-------------------------------------------------------------------------------------------------------
#function for scraping text file for certain pattern
def convertcsv(fname):
    errors = []
    linenum = 0
    pattern = re.compile(r"^\b[A-Z]{1}[A-Z]*")
    with open ('C:/Users/Hamad Nasir/Desktop/materials/texts/' + fname, 'rt') as myfile:
        for line in myfile:
            linenum += 1
            if pattern.search(line) != None:  # If pattern search finds a match,
                errors.append((linenum, line.rstrip('\n')))
                #create csvs folder in directory for simplicity
    with open('C:/Users/Hamad Nasir/Desktop/materials/'+fname+ '.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        title = fname
        writer.writerow([title])
        for err in errors:
            #for printing the scraped text from text file
            #print("Line ", str(err[0]), ": " + err[1])
            list = [[err[1]]]
            if len(err[1])>1:
                writer.writerows(list)
    csvFile.close()
#-------------------------------------------------------------------------------------------------
#function for converting multiple text files to csv file
def convertcsvMultiple(txtdir):
    for txt in os.listdir(txtDir): #iterate through pdfs in pdf directory
        fileExtension = txt.split(".")[-1]
        if fileExtension == "txt":
            txtFilename = txt
            text = txtFilename
            convertcsv(text)
#-----------------------------------------------------------------------------------------------
#convert pdf files folder to text files folder
convertMultiple(pdfDir, txtDir)
#convert text files folder to csv tables files folder
convertcsvMultiple(txtDir)

#convert csv files names
path = "C:/Users/Hamad Nasir/Desktop/materials/"
i = 0
for filename in os.listdir(path):
    if filename.endswith(".csv"):
        dst ="file" + str(i) + ".csv"
        src =path+ filename
        dst =path+ dst

        # rename() function will rename all the files
        os.rename(src, dst)
        i += 1

#place csv file name one by one to get corresponding sqlite file
subprocess.call("csvs-to-sqlite file0.csv file1.csv file2.csv file3.csv file4.csv file5.csv file6.csv file7.csv file8.csv file9.csv file10.csv file11.csv file12.csv file13.csv file14.csv file15.csv file16.csv file17.csv file18.csv file19.csv file20.csv file21.csv AllData.db",shell=True )
