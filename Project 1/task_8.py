# **************************************************************************** #
# Skyler Malinowski [ som12 ]
# Andrew Dos Reis [ ad1005 ]
# Project 1
# task_8.py
# CS 440
# **************************************************************************** #


# Import other Tasks
import task_1 as T1
import task_2 as T2
import task_3 as T3
import task_4 as T4
import task_5 as T5
import task_6 as T6
#import task_7 as T7
# Sys and Opt for CLI arguments and flags
import sys, getopt, os
# NumPy for math functions and data structures
import numpy as np
# Random for random numbers
import math
import random
# AnyTree to make and display Trees
from anytree import Node, RenderTree, AsciiStyle
from anytree.dotexport import RenderTreeGraph
# Regular Expression for string parsing
import re
# MatPlotLib for graphibg
import matplotlib.pyplot as plt
# Time for stopwatch
import time


# Task 8  **********************************************************************
def getBest(n):
    best_file = [None,0,0]
    fileList = [file for file in os.listdir() if '.txt' in file and 'T' not in file and '_k' in file]
    for file in fileList:
        file_n = file.split('_',1)  # split into n,k
        file_k = file_n[1]
        file_k = file_k[:-4]  # strip '.txt'
        file_n = file_n[0]
        file_n = int(file_n[1:])  # strip 'n'
        file_k = int(file_k[1:])  # strip 'k'
        if n is file_n and file_k > best_file[2]:
            best_file[0] = file
            best_file[1] = file_n
            best_file[2] = file_k
    return best_file


def saveBest(matrix,k,root,fileRoot=''):
    n = len(matrix)
    if fileRoot is '':
        fileName = 'n'+str(n)+'_k'+str(int(k))
    else:
        fileName = fileRoot+'_n'+str(n)+'_k'+str(int(k))
    if len(fileRoot) == 0:  # Unified file name
        fileList = [file for file in os.listdir() if ('.txt' in file or '.png' in file) and 'T' not in file and 'n'+str(n) in file and '_k' in file]
        if len(fileList) is 0:  # No files exist with that name
            T2.dumpFile(matrix,fileName)
            RenderTreeGraph(root).to_picture(fileName+'.png')
        else:  # Files exist with that name
            for file in fileList:
                file_n = file.split('_',1)
                file_k = file_n[1]
                file_k = file_k[:-4]
                file_n = file_n[0]
                file_n = int(file_n[1:])
                file_k = int(file_k[1:])
                if n is file_n and k > file_k:
                    os.remove(file)
                    T2.dumpFile(matrix,fileName)
                    RenderTreeGraph(root).to_picture(fileName+'.png')
    else:  # Task name system
        fileList = [file for file in os.listdir() if fileRoot in file and 'n'+str(n) in file and '_k' in file]
        if len(fileList) is 0:  # No files exist with that name
            T2.dumpFile(matrix,fileName)
            RenderTreeGraph(root).to_picture(fileName+'.png')
        else:  # Files exist with that name
            for file in fileList:
                file_n = file.split('_',4)
                file_k = file_n[3]
                file_k = file_k[:-4]
                file_k = int(file_k[1:])
                file_n = file_n[2]
                file_n = int(file_n[1:])
                if k > file_k:
                    os.remove(file)
                    T2.dumpFile(matrix,fileName)
                    RenderTreeGraph(root).to_picture(fileName+'.png')


# Main  ************************************************************************
def main(argv):
    # argv[1] = matrix size
    # argv[2] = iterations

    # Task 5 - RW
    p = 0.5
    # Task 6 - SA
    temperature = 1000
    tmp_decay = 0.999
    # Task 7 - GA

    t = [0,0]
    t[0] = time.time()
    for i in range(int(argv[2])):
        best_file = getBest(int(argv[1]))
        if best_file[0] is not None:
            matrix = T2.fileParse(best_file[0])
        else:
            matrix = T1.makeMatrix(int(argv[1]))
        new_matrix = T1.makeMatrix(int(argv[1]))
        new_k = T2.evaluate(new_matrix)
        print(i,"Evaluation Function =",new_k)
        if new_k >= best_file[2]:
            saveBest(new_matrix,new_k,None)
    '''
    if best_file[0] is not None:
        matrix = T2.fileParse(best_file[0])
    else:
        matrix = T1.makeMatrix(int(argv[1]))
    '''
    #best_file = getBest(int(argv[1]))
    #T3.collectData(matrix,argv[2])

    best_file = getBest(int(argv[1]))
    T5.collectData(matrix,argv[2],p)

    #best_file = getBest(int(argv[1]))
    #T6.collectData(matrix,argv[2],temperature,tmp_decay)

    #best_file = getBest(int(argv[1]))
    #T7.collectData(matrix,argv[2])

    t[1] = time.time()
    print("Total Elapsed Computational Time =",t[1]-t[0],"sec")

# run main module if not imported
if __name__ == "__main__":
	main(sys.argv)
