##########################################################################################################################################################################
#  Computer Project #9
#
#  Algorithm
#    importing necessary modules - string
#    writing function definition for the function open_file() which takes no arguments but returns a file pointer
#    writing function definition for the function read_file() which takes in one argument and returns a set
#    writing function definition for the function fill_completions() which takes in one argument and returns a dictionary
#    writing function definition for the function find_completions() which takes in 2 arguments and returns a set
#    writing function definition for the function main() which takes no arguments and works as the user interface and fulfills the requests by calling the above functions
#    special condition to call main
#
##########################################################################################################################################################################

import string    #importing necessary module - string module

def open_file():
    """
    Prompts the user for file name and does not leave the user until the user 
    enters a valid file name
    
    Parameters
    ----------
    None

    Returns
    -------
    file_obj : File Pointer
               A file object which serves as the connection between the file 
               in the computer and the python shell on which code is written
    """
    file_name= input("\nInput a file name: ") #inputting file name from the user
    while True:   #a while loop looping till the user enters the one which exists
        try:            #which exists -- here try except
            file_obj= open(file_name,"r", encoding="UTF-8")
            break
        except FileNotFoundError:   #This except will only catch FileNotFoundError
            print("\n[Error]: no such file") #this error will be displayed
            file_name= input("\nInput a file name: ") #for input of the filename
    return file_obj   #returning filepointer after all of this

def read_file(fp):
    '''
    From the recieved file pointer, it goes through the file line by line and
    then adds all the words to a set and then returns the set. The set contains
    all unique words and all in lower-case

    Parameters
    ----------
    fp : File Pointer
         File-pointer object

    Returns
    -------
    word_set : Set
               Set of words 

    '''
    word_set = set()           #the main set to be returned initialized
    str_punc = string.punctuation   #just the required thing from string module
    for line in fp:        #iterating through the file
        line=line.replace(" ",",")   #replacing all the places with a comma
        x=line.split(",")     #splitting and making it into a list
        c=0               #the variable which would govern the below while loop
        while c<len(x):       #the while loop begins
            k=x[c].strip(str_punc)      #stripping the unncessary punc
            k=k.strip(string.whitespace)  #stripping whitespace
            k = k.strip(str_punc)   #stripping the unncessary punc
            if k=='':           #if empty go here
                x.remove(x[c])   #remove that element
            else:            #or else come here
                x[c]=k           #change it to the required one
                c+=1             #increment only here
        word_list = x         #having assigning it to another list
        for i in range(len(word_list)):   #going through the list
            word_list[i] = word_list[i].lower().strip(str_punc) #doing the necessary
        for word in word_list:  #going through word by word
            flag = 0     #counter
            for letter in word:  #it is for avoiding the words having punc in between
                if letter in str_punc:
                    flag=1
                    break
            if flag==0 and len(word)!=1: #to avoid one letter
                word_set.add(word)  #adding to the set
    return word_set     #returning the set

def fill_completions(words):
    '''
    It accepts a set of words as an argument and it makes (the index,character)
    as a tuple and finds the corresponding set of words which have the 
    matching character at that particular index value and puts them as key:value
    pairs in the main dictionary which is to be returned

    Parameters
    ----------
    words : Set
            Set of words

    Returns
    -------
    new_dict :  Dictionary
                Dictionary containing key:value pairs as (index,character): set
                of matching words

    '''
    new_dict = {}        #initializing the dictionary
    for word in words:   #going through the words one by one
        for i in range(len(word)): #going through each word ch by ch
            ch_tup = (i, word[i])  #making ind:ch  tuples
            if ch_tup not in new_dict:  #avoid repition
                new_dict[ch_tup] = None #assigning none
    for keys in new_dict:  #going through the dictionary
        new_set = set()   #assigning new set
        for w in words:   #going through word by word
            try:           #try except to avoid the cases for Index out of range
                if w[keys[0]] == keys[1]:  #if matching, add
                    new_set.add(w)
            except IndexError:
                continue
        new_dict[keys]= new_set #changing the value from None to set
    return new_dict   #returns the dictionary


def find_completions(prefix, word_D):
    '''
    It accepts 2 arguments - the prefix and the dictionary(containing desired
    key:value pairs),it goes over the entire dictionary and looks for words
    with the desired prefix and if satisfied, will add to the set and finally
    returns that set

    Parameters
    ----------
    prefix : String
             The desired prefix as of the user
             
    word_D : Dictionary
             Dictionary containing key:value pairs as (index,character): set
             of matching words

    Returns
    -------
    new_wset : Set
               Set of words with the desired prefix

    '''
    ch_set = set()   #initializing the set
    new_wset = set()     #initializing the set
    additional_d = {}     #initializing the dictionary
    for ch in range(len(prefix)): #going through the prefix
        ch_tuple = (ch, prefix[ch])
        ch_set.add( ch_tuple)  #making (ind,ch) and add to set
    val_list = []   #helper list
    word_key = set(word_D.keys())   #to obtain set of keys only
    inter_section = word_key & ch_set   #finding the intersection
    len_imp = len(inter_section)    #the len of the intersection
    if inter_section != set() and len(inter_section)== len(ch_set): #the correct condition
        for ch_t in inter_section: #going through intersection
            val_set = word_D[ch_t]  #adding all the words to the list having 
            for val in val_set:      #-matching prefixes
                val_list+=[val]
        value_sets = set(val_list)  #having a set in another variable
        for ele in value_sets: #assigning them to 0
            additional_d[ele]= 0
        for element in val_list:  #if the elemnt there in the addional_d, add 1
            if element in additional_d:
                additional_d[element]+=1
        for k in additional_d:  #this is the most important to filter out the only and the 
            if additional_d[k]== len_imp:  #necssary words
                new_wset.add(k)
    return new_wset    #returns the set
    
def main(): #main function starts here
    """
    This is the main function which displays the various menu options and 
    performs the activities(calling the above written functions accordingly)
    which the user asks for and loops until the user wants to break.
    
    Parameters
    ----------
    None.

    Returns
    -------
    None.

    """
    file_obj = open_file()     #calling openifile for file-pointer
    word_set_val = read_file(file_obj)   #calling read-file to get the dictionary 
    pref_choice = input("\nEnter a prefix (# to quit): ") #prompt the user
    while True:   #the while  loop starts
        if pref_choice == "#":  #to break the loop, enter the pound symbol
            print("\nBye")  #closing message
            break       #break the loop
        else:    #if not pound symbol, come here
            answer_set = fill_completions(word_set_val) #calling appropriate function
            final_set = find_completions(pref_choice, answer_set) #calling appropriate function
            if final_set == set(): #if the set is empty
                print("\nThere are no completions.")  #print this
            else:   #if the set is not empty, come here
                print("\nThe words that completes {} are: {}".format(\
pref_choice,", ".join(sorted(final_set))))  #print it in a sorted, formatted way
            pref_choice = input("\nEnter a prefix (# to quit): ") #ask for user input


if __name__ == '__main__':     #special condition for this main
    main()















    
    
    
    
    
    
    
    
    
    
    
    
