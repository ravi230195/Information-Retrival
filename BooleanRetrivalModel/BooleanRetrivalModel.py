# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 14:25:00 2019

@author: ravik
"""

#from collections import defaultdict, OrderedDict
import sys,os

#    for v in token_dic
            
def processTokens(index_list, input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            tokens = line.split()
            doc_id = int(tokens[0])
            term_dic ={}
            term_freq_inc = round((float)(1/(len(tokens) - 1)), 6)
            for token in range(1,len(tokens)):
                if tokens[token] in term_dic.keys():
                    term_dic[tokens[token]][0] +=term_freq_inc 
                else:
                    term_dic[tokens[token]] = [term_freq_inc, doc_id]
            index_list.append(term_dic)
    return len(lines)

def calculateTF_IDF(i,idf):
    #print(i)
    for k in range(0,len(idf)):
        m = idf[k]
        for l in range(0, len(i[k])):
            (i[k][l])[0] = (i[k][l])[0]*m
            

    #print(i)
        
def createInvertedIndex(super_dic, doc_freq, dic):
    for k,v in dic.items():
        if k in super_dic.keys():
            super_dic[k].append(v)
            doc_freq[k] +=1
        else:
            super_dic[k] = [v]
            doc_freq[k] = 1

def createIDF(idf_dic, dic, total_num_docs):
    for k,v in dic.items():
        idf_dic[k] = round((float)(total_num_docs/v), 6)

def check_valid(current_itr, index_lengths):
    for i in range(0,len(current_itr)):
        #print("checking position {} ({} {})".format(i, current_itr[i], index_lengths[i]))
        if current_itr[i] > index_lengths[i]:
            return False
    return True

def update(current_itr, query_index_list, index_lengths):
    reached_end = []
    for i in range(0,len(current_itr)):
        if current_itr[i] > index_lengths[i]:
            reached_end.append(i)
    new_current_itr = []
    new_query_index_list = []
    new_index_length = []
    #print(reached_end)
    for k in range(0,len(current_itr)):
        if k not in reached_end:
            new_current_itr.append(current_itr[k])
            new_query_index_list.append(query_index_list[k])
            new_index_length.append(index_lengths[k])
    #print(new_current_itr, new_query_index_list ,new_index_length)
    return new_current_itr, new_query_index_list
    
def check_all_are_equal(current_itr, query_index_list):
    IDF = 0
    for i in range(0, len(current_itr) - 1):
        val1 = (query_index_list[i][current_itr[i]])[1]
        val2 = (query_index_list[i+1][current_itr[i+1]])[1]
        print("Trying to match {} {}".format(val1, val2))
        if val1 == val2:
            IDF = IDF + (query_index_list[i][current_itr[i]])[0]
            continue
        else:
            return False, []
    IDF = IDF + (query_index_list[len(current_itr) - 1][current_itr[len(current_itr) - 1]])[0]
    return True, [IDF, (query_index_list[i][current_itr[i]])[1]]

def calculateIDF(current_itr, query_index_list):
    IDF = 0
    for i in range(0, len(current_itr)):
        IDF = IDF + (query_index_list[i][current_itr[i]])[0]
    return IDF

def increment_iterator(current_itr, inc_all = False, increment_list = []):
    if (inc_all):
        for i in range(0, len(current_itr)):
            current_itr[i] +=1
    else:
        for i in range(0, len(increment_list)):
            current_itr[increment_list[i]] += 1
    #print("After incrementing {}".format(current_itr))

def find_lowest_index_value(current_itr, query_index_list, compare):
    increment_list = []
    min = 1000000
    for i in range(0, len(current_itr)):
        #print("comparing {} {}".format(min, (query_index_list[i][current_itr[i]])[1]))
        if min > (query_index_list[i][current_itr[i]])[1]:
            compare +=1
            min = (query_index_list[i][current_itr[i]])[1]
            increment_list.clear()
            increment_list.append(i)
        elif min == (query_index_list[i][current_itr[i]])[1]:
            #compare +=1
            increment_list.append(i)
    if len(increment_list) == len(current_itr):
        return True, [calculateIDF(current_itr, query_index_list), (query_index_list[0][current_itr[0]])[1]], increment_list, compare
    else:
        return False, 0, increment_list, compare
            
def rankingDoc(intersection_list):
    for i in range(0, len(intersection_list)):
        min = intersection_list[i][0]
        repalce = i
        for j in range(i, len(intersection_list)):
            if min < intersection_list[j][0]:
                min = intersection_list[j][0]
                repalce = j
        temp = intersection_list[repalce]
        intersection_list[repalce] = intersection_list[i]
        intersection_list[i] = temp

def add_doc_to_list(current_itr, increment_list, union_list, query_index_list):
    #if multiple are in increment list that means doc_ids are same.
    IDF = 0
    if len(increment_list) == 0:
        return
    for i in range(0, len(increment_list)):
        IDF = IDF + (query_index_list[increment_list[i]][current_itr[increment_list[i]]])[0]
    doc_val = (query_index_list[increment_list[0]][current_itr[increment_list[0]]])[1]
    union_list.append([IDF, doc_val])
    #print (union_list)
        
def calculateDAATAND(query_index_list):
    len_query_list = len(query_index_list)
    index_lengths = []
    intersection_list = []
    #print(query_index_list)
    #print(len_query_list)
    for i in range(0, len_query_list):
        index_lengths.append(len(query_index_list[i]) - 1)
    #print(index_lengths)
    current_itr = [0]*len(index_lengths)
    #print(current_itr)
    total_comparisions = 0
    while(check_valid(current_itr, index_lengths)):
        #print("validity check retuned true...")
        #matched, doc_id = check_all_are_equal(current_itr, query_index_list)
        matched , doc_id, increment_list , total_comparisions = find_lowest_index_value(current_itr, query_index_list, total_comparisions)
        if (matched):
            #print("mactched add to list...")
            #print(doc_id)
            intersection_list.append(doc_id)
            increment_iterator(current_itr, True)
        else:
            #increment_list = find_lowest_index_value(current_itr, query_index_list)
            increment_iterator(current_itr, False, increment_list)
    return intersection_list, total_comparisions

def calculateDAATOR(query_index_list, comparisions = 0, union_list = [], current_itr =[]):
    len_query_list = len(query_index_list)
    index_lengths = []
    #print(query_index_list)
    #print(len_query_list)
    for i in range(0, len_query_list):
        index_lengths.append(len(query_index_list[i]) - 1)
    #print(index_lengths)
    if len(current_itr) == 0:
        current_itr = [0]*len(index_lengths)
    #print(current_itr)
    
    while(check_valid(current_itr, index_lengths)):
        #print("validity check retuned true...")
        matched , doc_id, increment_list , comparisions = find_lowest_index_value(current_itr, query_index_list, comparisions)
        if (matched):
            #print("mactched add to list...")
            #print(doc_id)
            union_list.append(doc_id)
            increment_iterator(current_itr, True)
        else:
            add_doc_to_list(current_itr, increment_list, union_list, query_index_list)
            increment_iterator(current_itr, False, increment_list)
    current_itr, query_index_list = update(current_itr, query_index_list,  index_lengths)
    if len(current_itr) > 1:
        return calculateDAATOR(query_index_list, comparisions, union_list, current_itr)
    elif len(current_itr) == 1:
        #print((query_index_list[0][current_itr[0]:]))
        union_list =  union_list + (query_index_list[0][current_itr[0]:])
    #print("union intersection {}".format(union_list))
    #print("Total Comparisions {}".format(total_comparisions))
    return union_list, comparisions

def print_list_of_list(l):
        for k in range(0, len(l)):
            if k == len(l) - 1:
                print(l[k][1])
            else:
                print(l[k][1], end = " ")
def print_side_terms(terms):
    print(len(terms))
    for k in range(0,len(terms)):
        if k == len(terms) - 1:
            print(terms[k])
        else:
            print(terms[k], end = " ")
            
def print_ouput(terms, sorted_dic, idf_dic):
    i = []
    idf = []
    for term in terms:
        print("GetPostings")
        print(term)
        i.append(sorted_dic[term])
        idf.append(idf_dic[term])
        print("Postings list:", end =" ")
        print_list_of_list(sorted_dic[term])
    calculateTF_IDF(i,idf)
    intersection_list, total_comparisions_a = calculateDAATAND(i)
    print("DaatAnd")
    for k in range(0,len(terms)):
        if k == len(terms) - 1:
            print(terms[k])
        else:
            print(terms[k], end = " ")
    print("Results: ", end = "")
    if len(intersection_list) == 0:
        print("empty")
    else:
        print_list_of_list(intersection_list)
    print("Number of documents in results: {}".format(len(intersection_list)))
    print("Number of comparisons: {}".format(total_comparisions_a))
    print("TF-IDF")
    rankingDoc(intersection_list)
    print("Results:", end = " ")
    if len(intersection_list) == 0:
        print("empty")
    else:
        rankingDoc(intersection_list)
        print_list_of_list(intersection_list)
    union_list = []
    union_list, total_comparisions = calculateDAATOR(i, 0, union_list, [])
    print("DaatOr")
    for k in range(0,len(terms)):
        if k == len(terms) - 1:
            print(terms[k])
        else:
            print(terms[k], end = " ")
    print("Results: ", end = "")
    if len(union_list) == 0:
        print("empty")
    else:
        print_list_of_list(union_list)
    print("Number of documents in results: {}".format(len(union_list)))
    print("Number of comparisons: {}".format(total_comparisions))
    print("TF-IDF")
    print("Results:", end = " ")
    if len(union_list) == 0:
        print("empty")
    else:
        rankingDoc(union_list)
        print_list_of_list(union_list)

def query_processing(query_file, sorted_dic, idf_dic):
    with open(query_file, "r") as qf:
        lines = qf.readlines()
        for line in lines:
            tokens = line.split()
            print_ouput(tokens, sorted_dic, idf_dic)
            print("")

index_list = []
indexer = {}
doc_freq = {}
sorted_dic ={}
idf_dic = {}      

input_file = r'C:\Users\ravik\OneDrive\Desktop\IR\input_corpus.txt' #sys.argv[1]
output_file = r'C:\Users\ravik\OneDrive\Desktop\IR\output.txt' #sys.argv[2]
query_file = r'C:\Users\ravik\OneDrive\Desktop\IR\Project2_Sample_input.txt' #sys.argv[3]
total_num_docs = processTokens(index_list, input_file)

for i in index_list:
    createInvertedIndex(indexer, doc_freq, i)
sorted_keys = sorted(indexer.keys())
for i in sorted_keys:
    sorted_dic[i] = indexer[i]
createIDF(idf_dic, doc_freq, total_num_docs)

with open(output_file, 'w') as f:
    original = sys.stdout
    sys.stdout = f
    query_processing(query_file, sorted_dic, idf_dic)
    sys.stdout = original
   #print_ouput(['Elizabeth', 'creature'], sorted_dic, idf_dic)
