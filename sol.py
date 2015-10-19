# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 23:30:51 2015

@author: nghiatran
"""
import math
import random
import sys
from honeyGenWithSamples import *
from honeyGenNoSample import *
from word_rand import *


def read_password_files(filename, length=None):
    pw_list = [ ]
    f = open(filename)
    if length is not None:
        for i in range(length):
            line=f.next().strip()
            pw_list.append(tuple(line.split()))
    else:
        for line in f:
            pw_list.append(tuple(line.split()))          
    f.close()
    return pw_list

def sweetword_final_set1(input_password,n):
   sweetwords = generateBaseSweetWords(input_password,n-1)
   sweetwords.append(input_password)
   random.shuffle(sweetwords)
   return sweetwords

def sweetword_final_set2(weak_pw_list, input_password, n):
    sweetwords = []
    sweetwords = weak_sweetwords(weak_pw_list,input_password,n-1)
    if len(sweetwords) ==0:
        sweetwords = generateBaseSweetWords(input_password,n)
        sweetwords.append(input_password)
    else:
        for i in range(len(sweetwords), n-1):
            l = random.randint(7,10)
            sweetwords.append(random_markov_password(l))
    sweetwords.append(input_password)
    random.shuffle(sweetwords)
    return sweetwords
    
def sweetword_final_set3(long_pw_list,input_password):
    return[]

def main(input_filename,input_password):
    short_pw_list = read_password_files(input_filename,100)
    return sweetword_final_set2(short_pw_list,input_password,20)

def main(argv):
    l = len(argv)
    n = int(argv[1])
    input_filename = argv[2]
    output_filename = argv[3]
    
    algo = 1
    if l>4:
        algo = int(argv[4])
            
    if algo == 1:        
        print sweetword_final_set1("yellow",n-1)
    elif algo == 2:
        weak_pw_list = read_password_files("../rockyou-withcount.txt",100)
        print sweetword_final_set2(weak_pw_list,"mickey",n)
    else:
        print 'implement algo 3'


if __name__ == "__main__":
   main(sys.argv)


