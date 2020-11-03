import pandas as pd
import numpy as np

def Mean_and_var(data): #μ and #often represented by σ^2, s^2 or Var(X)
    _len = len(data)
    sum = 0
    for x in data:
        sum = sum + x
    mean = sum/_len
    var = 0
    for x in data:
        var = var + (x - mean)*(x - mean)
    var = (1/(_len - 1))*var
    return (mean, var)

def Gaussian(x, mean, var):
    f = np.exp(-((x-mean)*(x-mean))/(2*var))
    f = (1/np.sqrt(2*np.pi*var))*f
    return f

def Model_NB(data, header_decision, header_attrib = [], header_attrib_continuity = [], muy = 1):
    #muy is μ
    dict_model = {}
    value_decision = data[header_decision].tolist()
    len_value_decision = len(value_decision)
    label_decision = data[header_decision].unique().tolist()
    count_label = []
    for i in label_decision:
        count_label_diff = value_decision.count(i)
        count_label.append(count_label_diff)
    #
    df_decision = pd.DataFrame(data = [count_label],
                                columns = label_decision)
    #
    dict_attrib = {}
    for index in header_attrib:
        value_attrib = data[index].tolist()
        label_attrib = data[index].unique().tolist()
        len_label_attrib = len(label_attrib)
        #Laplace smoothing
        laplace = muy/len_label_attrib
        #
        df_attrib = pd.DataFrame(data = [],
                                    index = label_attrib,
                                    columns = label_decision)
        for x in label_decision:
            for y in label_attrib:
                sub_data = data[data[header_decision]==x]
                sub_data = sub_data[sub_data[index]==y]
                df_attrib[x][y] = ((len(sub_data)+laplace)/(df_decision[x][0]+muy))
        dict_attrib[index] = df_attrib
    #
    dict_attrib_continuity = {}
    for index in header_attrib_continuity:
        df_attrib_continuity = pd.DataFrame(data = [],
                                            index = ['mean', 'var'],
                                            columns = label_decision)
        for x in label_decision:
            sub_data = data[data[header_decision]==x]
            sub_data = sub_data[index]
            _mean, _var = Mean_and_var(sub_data)
            df_attrib_continuity[x]['mean'] = _mean
            df_attrib_continuity[x]['var'] = _var
        dict_attrib_continuity[index] = df_attrib_continuity
    #
    df_decision = df_decision/len_value_decision
    #
    dict_decision = {}
    dict_decision[header_decision] = df_decision
    #

    dict_model['decision'] = dict_decision
    dict_model['attrib'] = dict_attrib
    dict_model['attrib_continuity'] = dict_attrib_continuity
    #
    return dict_model

def Evaluation(record, model):
    for header, data in model['decision'].items():
        df_predict = data.copy()
    #
    for header, data in model['attrib'].items():
        for col in df_predict.columns:
            df_predict[col][0] = df_predict[col][0] * data.loc[record[header],:][col]
    #
    for header, data in model['attrib_continuity'].items():
        for col in df_predict.columns:
            x = record[header]
            mean = data.loc['mean'][col]
            var = data.loc['var'][col]
            df_predict[col][0] = df_predict[col][0] * Gaussian(x, mean, var)
    #
    return (df_predict.idxmax(axis = 1, skipna = True)[0])

def Train_and_eval(data, header_decision, header_attrib = [], header_attrib_continuity = [], ran_state = 0, split_ratio = 2/3):
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
    model = Model_NB(data_train, header_decision, header_attrib, header_attrib_continuity)
    #
    for i in range(rows):
        item = data_test.iloc[i,:]
        Y_data = item[header_decision]
        Y_test = Evaluation(item, model)
        # print(Y_test, Y_data)
        try:
            evaluation[Y_test][Y_data] += 1
        except KeyError:
            None
    return (evaluation)

if __name__ == "__main__":
    '''df = pd.read_csv("play_tennis.csv", encoding = 'utf-8', sep=',', index_col = 0)

    label_decision = 'play'
    label_attrib = ['outlook', 'wind']
    label_attrib_continuity = ['temp', 'humidity']
    class_positives = 'Yes'
    class_negatives = 'No'

    rows = df.shape[0]
    _class = df[label_decision].unique().tolist()
    #
    evaluation = pd.DataFrame(data = np.zeros((len(_class), len(_class)), dtype=int),
                            index = _class,
                            columns = _class)
    #
    model = Model_NB(df, label_decision, label_attrib, label_attrib_continuity)
    #
    for i in range(rows):
        item = df.iloc[i,:]
        Y_data = item[label_decision]
        Y_test = Evaluation(item, model)
        print(Y_test, Y_data)
        try:
            evaluation[Y_test][Y_data] += 1
        except KeyError:
            None
    # print(df)
    print(evaluation)'''

    label_decision = 'class'
    label_attrib = ['Gender', 'Polyuria', 'Polydipsia', 'sudden weight loss', 'weakness', 'Polyphagia', 'Genital thrush',
    'visual blurring', 'Itching', 'Irritability', 'delayed healing', 'partial paresis', 'muscle stiffness', 'Alopecia', 'Obesity']
    label_attrib_continuity = ['Age']
    df = pd.read_csv("../Report/diabetes_data_upload.csv", encoding = 'utf-8', sep=',')
    # print(Partition(df, label_attrib_continuity, label_decision))

    class_positives = 'Positive'
    class_negatives = 'Negative'
    count = 0
    average_F = 0
    average_accuracy = 0
    for i in range(1,11):
        print("Eval", i, ":")
        matrix = Train_and_eval(df, label_decision, label_attrib, label_attrib_continuity, ran_state = i)
        print(matrix)
        precision = (matrix[class_positives][class_positives])/ \
                        (matrix[class_positives][class_positives]+matrix[class_positives][class_negatives])
        #
        recall = (matrix[class_positives][class_positives])/ \
                    (matrix[class_positives][class_positives]+matrix[class_negatives][class_positives])
        #
        accuracy = (matrix[class_positives][class_positives]+matrix[class_negatives][class_negatives])/ \
                    (matrix[class_positives][class_positives]+matrix[class_negatives][class_negatives]+
                    matrix[class_positives][class_negatives]+matrix[class_positives][class_negatives])
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
