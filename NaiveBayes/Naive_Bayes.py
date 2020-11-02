import pandas as pd
import numpy as np

def variance(): #often represented by σ^2, s^2 or Var(X)
    return 0
def expectation(): #μ
    return 0

def model_NB(data, header_attrib, header_attrib_continuity, header_decision, muy = 1):
    #muy is μ
    value_decision = data[header_decision].tolist()
    len_value_decision = len(value_decision)
    label_decision = data[header_decision].unique().tolist()
    count_label = []
    for i in label_decision:
        count_label_diff = value_decision.count(i)
        # print(count_label_diff)
        count_label.append(count_label_diff)
    #
    df_decision = pd.DataFrame(data = [count_label],
                                columns = label_decision)
    list_df = []
    #
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
        list_df.append(df_attrib)
    #
    df_decision = df_decision/len_value_decision
    list_df.append(df_decision)
    #
    model_NB = pd.DataFrame(data = [list_df],
                            columns = header_attrib + [header_decision])

    return model_NB

def Evaluation(data, model):
    try:
        print()
    except ValueError:
        return 0
    return 0

def Train_and_eval(data, header_attrib, header_decision, ran_state, split_ratio = 2/3):
    data_train = data.sample(frac = split_ratio, random_state=ran_state)
    data_test = data.loc[~data.index.isin(data_train.index)]
    #
    rows = data_test.shape[0]
    _class = data[label_decision].unique().tolist()
    #
    evaluation = pd.DataFrame(data = np.zeros((len(_class), len(_class)), dtype=int),
                            index = _class,
                            columns = _class)
    #
    model = model_NB(data_train, header_attrib, header_decision)

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
    df = pd.read_csv("play_tennis.csv", encoding = 'utf-8', sep=',', index_col = 0)

    label_decision = 'play'
    label_attrib = ['outlook', 'temp', 'humidity', 'wind']
    label_attrib_continuity = 'Age'

    print(model_NB(df, label_attrib, label_decision)['outlook'][0]["Yes"]["Sunny"])
    #['outlook'][0].columns
    # numpyArray = np.array([[15, 22, 43],
    #                    [33, 24, 56]])
    #
    # panda_df = ["Column_1", "Column_2", "Column_3"] + ["Row_1", "Row_2"]
    #
    # print(panda_df)

    # numpyArray1 = np.array([[panda_df, 22, 43],
    #                    [33, 24, 56]])
    #
    # panda_df1 = pd.DataFrame(data = numpyArray1,
    #                     index = ["Row_1", "Row_2"],
    #                     columns = ["Column_1",
    #                                "Column_2", "Column_3"])
    #
    # print(panda_df1["Column_1"]["Row_1"]["Column_1"]["Row_1"])

    # sub_data = df[['outlook', 'temp']]
    # print(sub_data)
