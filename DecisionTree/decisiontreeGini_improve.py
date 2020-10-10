import pandas as pd
import numpy as np
import math

class TreeNode(object):
        def __init__(self, attrib, gini = 0, split_attribute = None, children = None):
            self.attrib = attrib                    # index of data in this node
            self.gini = gini                        # gini, will fill later
            self.split_attribute = split_attribute  # which attribute is chosen, it non-leaf
            self.children = children                # list of its child nodes

def Gini(data, header_decision):
    gini = 0
    value_decision = data[header_decision].tolist()
    #
    lenght = len(value_decision)
    label_decision = data[header_decision].unique().tolist()
    #function gini
    for i in label_decision:
        count_label_diff = value_decision.count(i)
        gini += math.pow(count_label_diff/lenght,2)
    return (1-gini)

def Info_continuity(data, header_attrib, header_decision, value_attrib_partitioned):
    #header_attrib : temp  ;
    info = 0
    value_attrib = data[header_attrib].tolist()
    #return len data
    lenght = len(value_attrib)
    #create sub_data with condition <= value_attrib_partitioned
    sub_data = data[data[header_attrib]<=value_attrib_partitioned]
    #Calculate lenght in sub data
    count_label_diff = len(sub_data)
    #Calculate Gini
    gini = Gini(sub_data, header_decision)
    #Calculate Info after Partition
    info += (count_label_diff/lenght)*gini
    #create sub_data with condition > value_attrib_partitioned
    sub_data = data[data[header_attrib]>value_attrib_partitioned]
    count_label_diff = len(sub_data)
    gini = Gini(sub_data, header_decision)
    info += (count_label_diff/lenght)*gini
    #
    return info

def Partition(data, header_attrib, header_decision):
    #Sort data by header_attrib (ex: age, temp)
    #header_attrib: temp ;header_decision: play
    info_partition = np.array([])
    value_partition = np.array([])
    data_sorted = data.sort_values(by=header_attrib)
    #get lenght of header_decision (ex: play)
    lenght = len(data_sorted[header_decision].tolist())
    for i in range(lenght-1):
        if(data_sorted.iloc[i][header_decision] != data_sorted.iloc[i+1][header_decision]):
            info_item = Info_continuity(data_sorted, header_attrib, header_decision, data_sorted.iloc[i][header_attrib])
            #Add in array info_partition
            info_partition = np.append(info_partition, info_item)
            #Add label_attrib_continuity of info_item in array value_partition
            value_partition = np.append(value_partition, data_sorted.iloc[i][header_attrib])
    #Postion min after Partition
    index_min_id = np.argmin(info_partition)
    #Value partition min at id min
    value_partition_min = value_partition[index_min_id]
    return value_partition_min
#
#

##================================##
def Info(data, header_attrib, header_decision):
    info = 0
    value_attrib = data[header_attrib].tolist()
    #return len data
    lenght = len(value_attrib)
    #
    label_attrib = data[header_attrib].unique().tolist()
    #
    for i in label_attrib:
        count_label_diff = value_attrib.count(i)
        sub_data = data[data[header_attrib]==i]
        gini = Gini(sub_data, header_decision)
        info += (count_label_diff/lenght)*gini
    return (info)

def Build_tree(data, header_attrib, header_decision):
    #child only one
    if(len(data[header_decision].unique().tolist())==1):
        return TreeNode(attrib = data.iloc[0][header_decision])
    gain = np.array([])
    for i in header_attrib:
        info = Info(data, i, header_decision)
        #Add node
        gain = np.append(gain, info)
    #Index min
    label_min_id = np.argmin(gain)
    #Creat attrib node
    node_attrib = header_attrib[label_min_id]
    node_gini = gain[label_min_id]
    #Remove node to be used
    header_attrib.remove(node_attrib)
    #Split attribute of node to be used
    split_attribute = data[node_attrib].unique().tolist()
    children = []
    for i in split_attribute:
        sub_data = data[data[node_attrib]==i]
        sub_node = Build_tree(sub_data, header_attrib, header_decision)
        children.append(sub_node)
    #
    node = TreeNode(attrib = node_attrib, gini = node_gini, split_attribute = split_attribute, children = children)
    #
    return (node)

def DrawTree(T, flag_draw=0):
    print(T.attrib, T.gini)
    if(T.split_attribute==None):
        None
    else:
        for i in range(len(T.split_attribute)):
            for j in range(flag_draw):
                print('\t\t', end='')
            print('   +--(', T.split_attribute[i],')--', end='')
            DrawTree(T.children[i], flag_draw+1)


if __name__ == "__main__":
    df = pd.read_csv("play_tennis_improve.csv", encoding = 'utf-8', sep=',', index_col = 0)

    label_decision = 'play'
    label_attrib = ['outlook', 'humidity', 'wind']
    label_attrib_continuity = 'temp'
    print(Partition(df, label_attrib_continuity, label_decision))

    # tree = Build_tree(df, label_attrib, label_decision)
    # DrawTree(tree)
    #data_sort = Sort_data(df, label_attrib_continuity))
    #df truyen du lieu
    #print(Info(df, 'outlook', label_decision))

#    tree = Build_tree(df, label_attrib, label_decision)
