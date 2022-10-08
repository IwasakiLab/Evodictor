def make_list(txtfile, delim="\t", column=0):
    names=[]
    with open(txtfile, 'r') as handle:
        for line in handle:
            names.append(line.split(delim)[column])
    return names

def make_hash1(txtfile,reverse=False,delim="\t"): # key -> value
    dic={}
    with open(txtfile,'r') as handle:
        for line in handle:
            line_list = line.split('\n')[0].split(delim)
            i=0; 
            if(not reverse):
                if(line_list[0] not in dic.keys()):
                    dic[line_list[0]]=line_list[1]
            else:
                if(line_list[1] not in dic.keys()):
                    dic[line_list[1]]=line_list[0]
    return dic

def make_hash2(txtfile,delim1="\t",delim2="\t",value_type="str"): # key -> [value1, value2, ...]
    dic={}
    with open(txtfile,'r') as handle:
        for line in handle:
            
            if(delim1==delim2): # key<del>value1<del>value2<del>...
                line_list = line.split('\n')[0].split(delim1)
                key       = line_list[0]
                values    = line_list[1:]
            else              : # key<del1>value1<del2>value2<del2>...
                key       = line.split('\n')[0].split(delim1)[0]
                values    = line.split('\n')[0].split(delim1)[1].split(delim2)
            
            # modify type when needed
            if(value_type!="str"):
                type_modified_values = []
                for elem in line_list[1:]:
                    if(value_type=="int"):
                        type_modified_values.append (int  (elem))
                    if(value_type=="float"):
                        type_modified_values.append (float(elem))
                values    = type_modified_values
            
            # register the key-values pair in a dictionary
            if(key not in dic.keys()):
                dic[key]  = values
            else:
                dic[key].extend(values)

    return dic

def make_hash3(txtfile, key_column, value_column, reverse=False,delim="\t",value_type="str"): # key -> [value1, value2, ...]
    dic={}
    with open(txtfile,'r') as handle:
        for line in handle:
            line_list = line.split('\n')[0].split(delim)
            key       = line_list[key_column]
            value     = line_list[value_column]
            if (value_type != "str"):
                if  (value_type == "int"  ):
                     value        =  int  (value)
                elif(value_type == "float"):
                     value        =  float(value)
            try:
                dic[key].append(value)
            except:
                dic[key]=[value]
    return dic

def connect_dict(dic1, dic2):
    dic={}
    for dic1_key in dic1.keys():
        if(dic1[dic1_key] in dic2.keys()):
            dic[dic1_key]=dic2[dic1[dic1_key]]
        #else:
        #    print("no key named "+dic1[dic1_key]+" in dic2")
    return dic

def reverse_dict(dic):
    outdic={}
    for key in dic.keys():
        if(dic[key] not in outdic.keys()):
            outdic[dic[key]]=key
        #else:
        #    print("multiple identical values: "+dic[key])
    return outdic

def make_set_of_lists(pair_list_file, keys_of_interest_file=None, values_of_interest_file=None):
    
    dic = make_hash2(pair_list_file)
    list_of_set = []
    
    if(keys_of_interest_file!=None):
        keys_of_interest=make_list(keys_of_interest_file)
    else:
        keys_of_interest=list(dic.keys())
    
    if(values_of_interest_file!=None):
        values_of_interest=make_list(values_of_interest_file)
    else:
        values_of_interest=set()
        for value_list in list(dic.values()):
            values_of_interest = values_of_interest | set(value_list)
        
    for elem in keys_of_interest:
        print(list( set(dic[elem]) & set(values_of_interest) ))
        list_of_set.append({'name':elem, 'node_list':list( set(dic[elem]) & values_of_interest )})
    
    return list_of_set

def export_hash(myhash, delim="\t", value_type=None):
    if(value_type == "list"):
        for key in sorted(myhash.keys()):
            print(str(key) + delim[0], end="")
            for value in myhash[key]:
                print(str(value) + delim[1], end="")
            print("")
    else:
        for key in sorted(myhash.keys()):
            print(str(key) + delim + str(myhash[key]))