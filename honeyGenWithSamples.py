# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 22:06:10 2015

@author: nghiatran
"""
import random
## Generate maximum n weak honeywords, excluding the input password
def weak_sweetwords(weak_pw_list, input_password, n):
    list_len = len(weak_pw_list)
    n = min(9,n)
    sweetwords =[] 
    i=0
    
    while True:
        if i >= list_len:
            break;
        ## find a case-insensitive match in the list. 
        if len(weak_pw_list[i]) == 2 and input_password.find(weak_pw_list[i][1]) != -1:
            break;
        i = i+1
        
    #if the input password is not a popular password
    if i >= list_len:
        return [];

    ## add passwords that have similar popularity 
    if i<=5:
        for j in range(random.randint(0,5), n):
            if i!= j:
                sweetwords.append(input_password.replace(weak_pw_list[i][1],weak_pw_list[j][1]))
    else:
        upper_position_bound = random.randint(i,min(i+4,list_len-1))
        for j in range(upper_position_bound-n+1, upper_position_bound+1):
            if i!= j:
                sweetwords.append(input_password.replace(weak_pw_list[i][1],weak_pw_list[j][1]))
    
    random.shuffle(sweetwords)
    return sweetwords

