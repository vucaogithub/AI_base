'''author https://github.com/NguyenDuyKha'''
import pandas as pd
import numpy as np

class TreeNode(object):
    def __init__(self, attrib, entropy = 0, split_attribute = None, children = None):
        self.attrib = attrib                    # index of data in this node
        self.entropy = entropy                  # entropy, will fill later
        self.split_attribute = split_attribute  # which attribute is chosen, it non-leaf
        self.children = children                # list of its child nodes

def Entropy(data, header_decision):
    entropy = 0
    value_decision = data[header_decision].tolist()
    lenght = len(value_decision)
    label_decision = data[header_decision].unique().tolist()
    for i in label_decision:
        count_label_diff = value_decision.count(i)
        entropy += -(count_label_diff/lenght)*np.log2(count_label_diff/lenght)
    return (entropy)

def Info(data, header_attrib, header_decision):
    info = 0
    #
    value_attrib = data[header_attrib].tolist()
    #
    lenght = len(value_attrib)
    #
    label_attrib = data[header_attrib].unique().tolist()
    #
    for i in label_attrib:
        count_label_diff = value_attrib.count(i)
        sub_data = data[data[header_attrib]==i]
        entropy = Entropy(sub_data, header_decision)
        info += (count_label_diff/lenght)*entropy
    return (info)

def Build_tree(data, header_attrib, header_decision):
    entropy = Entropy(data, header_decision)
    if(entropy==0):
        return TreeNode(attrib = data.iloc[0][header_decision])
    gain = np.array([])
    for i in header_attrib:
        info = Info(df, i, header_decision)
        gain = np.append(gain, (entropy-info))
    #index max
    label_max_id = np.argmax(gain)
    #
    node_attrib = header_attrib[label_max_id]
    node_entropy = gain[label_max_id]
    #
    header_attrib.remove(node_attrib)
    #
    split_attribute = data[node_attrib].unique().tolist()
    children = []
    for i in split_attribute:
        sub_data = data[data[node_attrib]==i]
        sub_node = Build_tree(sub_data, header_attrib, header_decision)
        children.append(sub_node)
    #
    node = TreeNode(attrib = node_attrib, entropy = node_entropy, split_attribute = split_attribute, children = children)
    #
    return (node)


def DrawTree(T, flag_draw=0):
    print(T.attrib)
    if(T.entropy==0):
        None
    else:
        for i in range(len(T.split_attribute)):
            for j in range(flag_draw):
                print('\t\t', end='')
            print('   +--(', T.split_attribute[i] ,')--', end='')
            DrawTree(T.children[i], flag_draw+1)

if __name__ == "__main__":
    df = pd.read_csv("play_tennis.csv", encoding = 'utf-8', sep=',', index_col = 0)

    label_decision = 'play'
    label_attrib = ['outlook', 'temp', 'humidity', 'wind']
    tree = Build_tree(df, label_attrib, label_decision)
    DrawTree(tree)

    #==========================#
    # print(tree.children[0].attrib)
    # print('outlook')
    # print('   +--', '(sunny)', '--', 'humidity')
    # print('\t\t', end='')
    # print('\t\t', '1')
    #==========================#
    # a = TreeNode('hello')
    # list_a = []
    # list_a.append(a)
    # print(list_a[0].attrib)
    #==========================#
    # is_sunny = df['outlook']=='Sunny'
    # temp = df[is_sunny]
    # print(temp)

    # temp_1 = df[df.outlook.eq('Sunny')]
    # print(temp_1)
    #==========================#
    # label_attrib.remove('outlook')
    # print(label_attrib)
    #print(df.iloc[0]['play'])
    #==========================#
    # entropy = Entropy(df, label_decision)
    # gain = np.array([])
    # for i in label_attrib:
    #     info = Info(df, i, label_decision)
    #     gain = np.append(gain, (entropy-info))
    # label_max_id = np.argmax(gain)
    # print(label_attrib[label_max_id])
    #==========================#
    # entropy =
    # values = df['outlook'].unique().tolist()
    # print(values)
