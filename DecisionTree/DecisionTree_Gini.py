import pandas as pd
import numpy as np
import math

class TreeNode(object):
        def __init__(self, attrib, gini = 0, split_attribute = None, children = None):
            self.attrib = attrib                    # index of data in this node
            self.gini = gini                        # gini, will fill later
            self.split_attribute = split_attribute  # which attribute is chosen, it non-leaf
            self.children = children                # list of its child nodes

def Sort_data(data, header_attrib ):
    #Sort data by header_attrib (ex: age, temp)
    data_sorted = data.sort_values(by=header_attrib)
    return data_sorted

def Gini(data, header_decision):
    gini = 0
    value_decision = data[header_decision].tolist()
    #
    lenght = len(value_decision)
    label_decision = data[header_decision].unique().tolist()
    #
    for i in label_decision:
        count_label_diff = value_decision.count(i)
        gini += math.pow(count_label_diff/lenght,2)
    return (1-gini)

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
    print(header_attrib)
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
        sub_node = Build_tree(sub_data, header_attrib.copy(), header_decision)
        children.append(sub_node)
    #
    node = TreeNode(attrib = node_attrib, gini = node_gini, split_attribute = split_attribute, children = children)
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
    df = pd.read_csv("play_tennis.csv", encoding = 'utf-8', sep=',', index_col = 0)

    label_decision = 'play'
    label_attrib = ['outlook', 'temp', 'humidity', 'wind']
    tree = Build_tree(df, label_attrib, label_decision)
    DrawTree(tree)
