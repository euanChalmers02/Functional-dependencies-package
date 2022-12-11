import random

def next_alpha(s):
    return chr((ord(s.upper())+1 - 65) % 26 + 65).upper()

def generateQuestion(numAttributes,NumFDS,seed):
    list_attributes = []
    list_attributes.append(seed)
    list_FDS = []
    for k in range(numAttributes):
        list_attributes.append(next_alpha(list_attributes[k]))
        
    for y in range(NumFDS):
#         remove same eg.g A->A
        if y%2==0:
            temp_FD = str(random.choice(list_attributes)+","+random.choice(list_attributes)+"->"+ random.choice(list_attributes))
            list_FDS.append(temp_FD)
        else:
            temp_FD = str(random.choice(list_attributes)+"->"+ random.choice(list_attributes))
            list_FDS.append(temp_FD)
            
    print(list_FDS)
    print(list_attributes)
    return(list_attributes,list_FDS)

def checkClosureAnswer(attributes,fds,answer_closure):
    ALG_Closure = closureALG(attributes,fds)
    
    ALG_Closure.sort()
    answer_closure.sort()
    
    if ALG_Closure == answer_closure:
        return True
    else:
        print("FALSE - correct answer was : ",ALG_Closure)
        return False
    
def closureALG(attributes,fds):
    closure = attributes.copy()
    unused = fds.copy()
    ind = True
    
    while(ind == True):
        ind = False
        for elm in unused:
            temp_fds_split = elm.split("->")
            temp_LHS = temp_fds_split[0]
            temp_RHS = temp_fds_split[1]
            temp_LHS = temp_LHS.split(",")
            sub_inc = False
            for one in temp_LHS:
                if one not in closure:
                    sub_inc = True
            
            if sub_inc == False:
                unused.remove(elm)
                closure = closure + (temp_RHS.split(","))
                ind = True
    
    closure = list(dict.fromkeys(closure))
    return closure


def BCNF(attributes_input,fds_input):
    parent_flag = True
    
    for elt in fds_input:
        temp_fds_split = elt.split("->")
        temp_LHS = temp_fds_split[0]
        temp_RHS = temp_fds_split[1]
        temp_RHS = temp_RHS.split(",")
        temp_LHS = temp_LHS.split(",")
        
        flag = True
        for tr in temp_RHS:
            if tr  not in temp_LHS:
                flag = False
    
        if flag == False:
            flag = True
            res = (closureALG(temp_LHS,fds_input))
            if sorted(res) != sorted(attributes_input):
                flag = False
                print(elt ," does not compy with BCNF -> is not a super key")
                
    
        if flag == False:
            parent_flag = False
            break
            
    return parent_flag

def checkBCNFAnswer(attributes,fds,answer_BCNF):
    BCNF_aws = BCNF(attributes,fds)
    
    if BCNF_aws == answer_BCNF:
        return True
    else:
        print("FALSE - correct answer was : ",ALG_Closure)
        return False
    
def add_edge(source,dest,graph):
    if source in graph:
        local = (graph[source])
        local.append(dest)
        graph[source] = local
    else:
        graph[source] = [dest]
        
    if dest not in graph:
        add_node(dest,graph)

def add_node(node,graph):
    graph[node] = []
    
def remove_nodes(to_remove,graph):
    for one in to_remove:
        del graph[one]
    
def build_layer(graph):
    list_to_op = []
    for node in graph:
        if graph[node] == []:
            list_to_op.append(node)
    
    for em in list_to_op:
        for item in list_to_op:
            new_local_node = str(em+item)
            if item != em and new_local_node[::-1] not in graph:
                add_edge(em,new_local_node,graph)
    
    to_remove = []
    for single in graph:
        if len(set(single)) != len(single):
            to_remove.append(single)
            
#     does not remove the edge correctly yet 
    remove_nodes(to_remove,graph)
        
def ck(attributes,input_FD):
    ck = []
    graph = {}
    
#     start to build the graph
    add_node("o",graph)
    for elt in attributes:
        add_edge("o",elt,graph)
    
    for y in range(len(attributes)):
        build_layer(graph)
    
#     start checks
    while(len(graph)>0):
        key = list(graph.keys())[0]
        result = closureALG([key],input_FD)
        if sorted(result) == sorted(attributes):
            ck.append(key)
            to_remove = graph[key]
            to_remove.append(key)
            remove_nodes(to_remove,graph)
        else:
            remove_nodes([key],graph)
      
    return ck       

def isPrime(temp_RHS,attributes,input_FD):
    master_flag = True
    c_keys = ck(attributes,input_FD)
    for one in temp_RHS:
        print(one)
        flag_prime = False
        for each in c_keys:
            if one in each:
                flag_prime = True
                break
                
        if flag_prime != True:
            master_flag = False
            break
    
    return master_flag

# find all the prime attributes and then run bcnf and fall back to rest of the method
def threeNF(attributes,input_FD):
#     all the same as bcnf
    parent_flag = True
    for elt in input_FD:
        temp_fds_split = elt.split("->")
        temp_LHS = temp_fds_split[0]
        temp_RHS = temp_fds_split[1]
        temp_RHS = temp_RHS.split(",")
        temp_LHS = temp_LHS.split(",")
        
        flag = True
        for tr in temp_RHS:
            if tr  not in temp_LHS:
                flag = False
    
        if flag == False:
            flag = True
            res = (closureALG(temp_LHS,input_FD))
            if sorted(res) != sorted(attributes):
#                 added for the thrid requirment
                flag = (isPrime(temp_RHS,attributes,input_FD))
                print(elt ," does not compy with 3NF -> is not a key or prime on LHS")
                
        if flag == False:
            parent_flag = False
            break
            
    return parent_flag

def checkCK(attributes,input_FD,answer):
    if sorted(ck(attributes,input_FD)) == sorted(answer):
        return True
    else:
        print("ERROR - expected answer was ",sorted(ck(attributes,input_FD))," vs ",sorted(answer))
        return False

def isCompleteClosure(attributes,input_FD,curr_FD):
    LHS = curr_FD.split("->")
    LHS = LHS[0]
    LHS = LHS.split(",")
    if sorted(closureALG(LHS,input_FD)) == sorted(attributes):
        print("is a compleate closure")
        return True
    else:
        print("incompleate closure")
        return False
    
# should be of form "x -> yz = x -> y"
def simplifyDECOMP(equation):
    EQ_split = equation.split("=")
    decomp = EQ_split[0]
    aim = EQ_split[1]
    aim_split = aim.split("->")
    
    print("1) ",decomp," [given]")
    decomp = decomp.split("->")
    reflex = str(decomp[1]+"->"+ aim_split[1])
    print("2) ",reflex , " [refleivity]")
    print("3) ",aim ," [transivity 1 & 2]")
    
def ReadMe():
    info = "This is my python function to help learn functional dependecies and normal forms in dbms \nThanks and enjoy, Euan Chalmers \n\nStill in progress: \n*3NF synthesis \n*MinimalCover "
    size = 50
    print("-"*size)
    print(info)
    print("-"*size)

def Help():
    help_info = """ This is where i will describe each of the methods"""
    size = 50
    print("-"*size)
    print(help_info)
    print("-"*size)

def AxiomProof():
    print("Proof of decompisition :")
    print("x -> yz = x -> y")
    print("1) x -> yz  [given]")
    print("2) yz -> y  [reflexivity]")
    print("3) x-> y    [transivity 1 & 2]")
    print("******************")
    
    print("Proof of Union : ")
    print("{x -> y,x -> z} = x -> yz  ")
    print("1) x -> y    [given]")
    print("2) x -> z    [given]")
    print("3) x -> xz   [augmentation with 2 by x]")
    print("4) xz -> zy  [augmentation with 1 by z]")
    print("5) x -> yz   [transivity using 3 & 4]")
    
    print("******************")
    print("In the exam write down all essentail axioms and the proofs")
    
    
def minimalFDS(attributes,FDS):
    newFDS = []
#     part 1 simply each of the RHS using armstrong decompisition
    for each in FDS:
        temp = each.split("->")
        LHS = temp[0]
        RHS = temp[1]
        RHS = RHS.split(",")
        for elt in RHS:
            newFDS.append(str(LHS+"->"+elt))
    
    print(newFDS)
    print("helloe")
    
#     part 2 simplify any of the RHS of new list of FD's
    for each in newFDS:
        temp = each.split("->")
        LHS = temp[0]
        RHS = temp[1]
        LHS = LHS.split(",")
        if len(LHS) >1:
            print("*** to do : ",each)
            if(isCompleteClosure(attributes,newFDS,each)!= True):
                print(each , " this need to be reduced as isnt a ck")
#                 need to add working here 
            else:
                print(each," is complete")
    
    nextFDS = newFDS.copy()
# part 3 check if any can be removed (run the entailment on each) and remove in yes
    print("The follwoing should be written as step 3 in the exam")
    to_remove = []
    for each in nextFDS:
        temp_arr = nextFDS.copy()
        temp_arr.remove(each)
        if (isCompleteClosure(attributes,temp_arr,each) == True):
            to_remove.append(each)
        print(nextFDS , " !|= ",each, " == ",isCompleteClosure(attributes,temp_arr,each) )
        
    for each in to_remove:
        nextFDS.remove(each)
        
    return nextFDS
    
def threenfSynthesisALG(attributes,FDS):
    rough_working_dict = {}
    
    preWork = minimalFDS(attributes,FDS)
    
    # part 1 group by the lhs
    for each in preWork:
        temp = each.split("->")
        LHS = temp[0]
        RHS = temp[1]
        if LHS not in rough_working_dict.keys():
            rough_working_dict[LHS] = RHS
        else: 
            temp = rough_working_dict[LHS]
            rough_working_dict[LHS] = temp + ","+RHS
            
    print(rough_working_dict)
    
# part 2 write the attributes for each of the FDS
    result = []
    for key in rough_working_dict:
        att = str(key + ","+rough_working_dict[key])
        print("("+att+"  "+key," -> ",rough_working_dict[key],")")
        result.append(str(att+" {  "+key+" -> "+rough_working_dict[key]))
    
    return result
    
def parseInputEach(FDs):
    attributes = (set(FDs))
    attributes.remove(">")
    attributes.remove("-")
    attributes.remove(",")
    attributes = (list(attributes))
    
    liste = FDs.split(",")
    new_FDS = []
    for each in liste:
        temp_FD = ""
        
        temp = each.split("->")
        LHS = temp[0]
        RHS = temp[1]
        
        for elt in LHS:
            temp_FD = temp_FD + elt + ","
        temp_FD = temp_FD[:-1]
        temp_FD = temp_FD + "->"
        for one in RHS:
            temp_FD = temp_FD + one + ","
        temp_FD = temp_FD[:-1]
        new_FDS.append(temp_FD)
        
    return (new_FDS,attributes)
    