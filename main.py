# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 23:30:51 2015

@author: nghiatran
"""
import math
import random


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


def sweetwords2(short_pw_list, input_password):
    sweetwords =[input_password] 
    i=0
    while i < 100:
        if short_pw_list[i][1].lower() == input_password.lower():
            break;
        i = i+1
        
    #if the input password is not a popular password
    if i > 99:
        return; ## to integrate with algo 1
        
    ## add passwords that have similar popularity to the real password
    if i<=5:
        for j in range(0, 10):
            if i!= j:
                sweetwords.append(short_pw_list[j][1])
    else:
        upper_position_bound = min(i+4,99)
        for j in range(upper_position_bound-9, upper_position_bound+1):
            if i!= j:
                sweetwords.append(short_pw_list[j][1])
    print i
    random.shuffle(sweetwords)
    return sweetwords

def main(input_filename,input_password):
    short_pw_list = read_password_files(input_filename,100)
    return sweetwords2(short_pw_list,input_password)
    
print main("../rockyou-withcount.txt","mickey")
    


