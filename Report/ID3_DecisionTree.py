import pandas as pd
import numpy as np

class TreeNode(object):
        def __init__(self, attrib, entropy = 0, split_attribute = None, children = None):
            self.attrib = attrib                    # index of data in this node
            self.entropy = entropy                  # entropy, will fill later
            self.split_attribute = split_attribute  # which attribute is chosen, it non-leaf
            self.children = children                # list of its child nodes

def Entropy(data, header_decision): #header_decision = 'play'
    entropy = 0
    value_decision = data[header_decision].tolist()
    #
    lenght = len(value_decision)
    label_decision = data[header_decision].unique().tolist()
    #
    for i in label_decision:
        count_label_diff = value_decision.count(i)
        entropy += -(count_label_diff/lenght)*np.log2(count_label_diff/lenght)
    return (entropy)
#======================
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
    #Calculate entropy
    entropy = Entropy(sub_data, header_decision)
    #Calculate Info after Partition
    info += (count_label_diff/lenght)*entropy
    #create sub_data with condition > value_attrib_partitioned
    sub_data = data[data[header_attrib]>value_attrib_partitioned]
    count_label_diff = len(sub_data)
    entropy = Entropy(sub_data, header_decision)
    info += (count_label_diff/lenght)*entropy
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
#======================
def Info(data, header_attrib, header_decision): #header_attrib = 'outlook', 'temp'...
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

def Non_homogeneous(data, header_decision):
    radio_stand = 1.0
    value_decision = data[header_decision].tolist()
    #List value decision
    label_decision = data[header_decision].unique().tolist()
    #Array ratio and count_label_diff
    count_label_diff = []
    radio = []
    for i in label_decision:
        count_label_diff.append(value_decision.count(i))
    #Take id value min in count_label_diff Array
    label_id_min = np.argmin(count_label_diff)
    #Take value min in count_label_diff array
    value_min = count_label_diff[label_id_min]
    #Take value in count_label_diff array div value min in count_label_diff array -> add radio array
    for i in count_label_diff:
        radio.append(i/value_min)
    #Take index of value max in radio array
    radio_id_max = np.argmax(radio)
    radio_max = radio[radio_id_max]
    #Value max in radio array
    if(radio.count(radio_max) >= 2 and radio_max >= radio_stand):
        return None
    else:
        return label_decision[radio_id_max]
#========================
def Build_tree(data, header_attrib, header_decision):
    entropy = Entropy(data, header_decision)
    if(len(header_attrib) == 0 and entropy != 0):
        # Var homog save value Non_homogeneous
        homog = Non_homogeneous(data, header_decision)
        if(homog == None):
            return None
        else:
            return TreeNode(attrib = homog)
    #
    #
    elif(entropy==0):
        return TreeNode(attrib = data.iloc[0][header_decision])
    #
    gain = np.array([])
    for i in header_attrib:
        info = Info(data, i, header_decision)
        #
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
        sub_node = Build_tree(sub_data, header_attrib.copy(), header_decision)
        if(sub_node == None):
            #
            return Build_tree(data, [], header_decision)
        children.append(sub_node)
    #
    node = TreeNode(attrib = node_attrib, entropy = node_entropy, split_attribute = split_attribute, children = children)
    return (node)

def DrawTree(T, flag_draw=0):
    print(T.attrib, T.entropy)
    if(T.entropy==0):
        None
    else:
        for i in range(len(T.split_attribute)):
            for j in range(flag_draw):
                print('\t\t', end='')
            print('   +--(', T.split_attribute[i] ,')--', end='')
            DrawTree(T.children[i], flag_draw+1)

def Evaluation(data, tree):
    split_attribute = data[tree.attrib]
    try:
        index_split_split_attribute = tree.split_attribute.index(split_attribute)
    except ValueError:
        return None
    tree = tree.children[index_split_split_attribute]
    if(tree.children == None):
        return tree.attrib
    return Evaluation(data, tree)

def Train_and_eval(data, header_attrib, header_decision, ran_state, split_ratio = 2/3):
    data_train = data.sample(frac = split_ratio, random_state=ran_state)
    data_test = data.loc[~data.index.isin(data_train.index)]
    #
    rows = data_test.shape[0]
    _class = data[header_decision].unique().tolist()
    #
    evaluation = pd.DataFrame(data = np.zeros((len(_class), len(_class)), dtype=int),
                            index = _class,
                            columns = _class)
    #
    tree = Build_tree(data_train, header_attrib, header_decision)
    # DrawTree(tree)
    #
    for i in range(rows):
        item = data_test.iloc[i,:]
        Y_data = item[header_decision]
        Y_test = Evaluation(item, tree)
        # print(Y_test, Y_data)
        try:
            evaluation[Y_test][Y_data] += 1
        except KeyError:
            None
    return (evaluation)

if __name__ == "__main__":
    label_decision = 'class'
    label_attrib = ['Age', 'Gender', 'Polyuria', 'Polydipsia', 'sudden weight loss', 'weakness', 'Polyphagia', 'Genital thrush',
    'visual blurring', 'Itching', 'Irritability', 'delayed healing', 'partial paresis', 'muscle stiffness', 'Alopecia', 'Obesity']
    # label_attrib_continuity = 'Age'
    df = pd.read_csv("diabetes_data_upload_v1.csv", encoding = 'utf-8', sep=',')
    # print(Partition(df, label_attrib_continuity, label_decision))

    class_positives = 'Positive'
    class_negatives = 'Negative'
    count = 0
    average_F = 0
    average_accuracy = 0
    for i in range(1,11):
        print("Eval", i, ":")
        matrix = Train_and_eval(df, label_attrib.copy(), label_decision, i)
        print(matrix)
        precision = (matrix[class_positives][class_positives])/ \
                        (matrix[class_positives][class_positives]+matrix[class_positives][class_negatives])
        #
        recall = (matrix[class_positives][class_positives])/ \
                    (matrix[class_positives][class_positives]+matrix[class_negatives][class_positives])
        #
        accuracy = (matrix[class_positives][class_positives]+matrix[class_negatives][class_negatives])/ \
                    (matrix[class_positives][class_positives]+matrix[class_negatives][class_negatives]+ \
                    matrix[class_positives][class_negatives]+matrix[class_negatives][class_positives])
        print('Accuracy:', accuracy)
        F = (2*precision*recall)/(precision+recall)
        print('F:\t', F)
        #
        average_accuracy += accuracy
        average_F += F
        #
        count += 1
    #
    print('Average Accuracy:', average_accuracy/count)
    print('Average_F:\t', average_F/count)

    # Train_and_eval(df, label_attrib, label_decision, 5)
