# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 22:06:10 2015

@author: nghiatran
"""
import random
## Generate maximum n weak honeywords, excluding the input password
def weak_sweetwords(weak_pw_list, input_password, n):
    n = min(9,n)
    sweetwords =[] 
    i=0
    while i < 100:
        ## find a case-insensitive match in the list. 
        if weak_pw_list[i][1].lower() == input_password.lower():
            break;
        i = i+1
        
    #if the input password is not a popular password
    if i > 99:
        return [];

    ## add passwords that have similar popularity 
    if i<=5:
        for j in range(0, n):
            if i!= j:
                sweetwords.append(weak_pw_list[j][1])
    else:
        upper_position_bound = random.randint(i,min(i+4,99))
        for j in range(upper_position_bound-n+1, upper_position_bound+1):
            if i!= j:
                sweetwords.append(weak_pw_list[j][1])
    
    random.shuffle(sweetwords)
    return sweetwords

