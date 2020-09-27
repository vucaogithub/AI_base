import pandas as pd
import math


class Node:
  def __init__(self, attrib, label, node):
    self.attrib = attrib
    self.label = label
    self.node = Node

def Count_label(data, header_label):
    column = data[header_label]
    sum = len(column)
    # count value of label
    count = {}
    for i in column:
        if i in count:
            count[i] += 1
        else:
            count[i] = 1
    return sum, count
def Entropy(data, header_label):
    sum, count = Count_label(data, header_label)
    entropy = 0
    #sorted function sap xep theo key voi reverse=True thì sắp xếp theo giá trị giảm dần, nguoc lai tăng dần.
    for i in sorted(count, key=count.get, reverse=False):
        # print(i, count[i])
        entropy += -(count[i]/sum)*math.log2(count[i]/sum)
    print(entropy)

def Gain(data, header_label):
    sum, count = Count_label(data, header_label)
    print(sum)
    for i in sorted(count, key=count.get, reverse=False):
        print(i, count[i])
    data_temp = list(filter(lambda x, x = 'Sunny', data))
    print(data_temp)
def main():
    data = pd.read_csv("play_tennis.csv",encoding = 'utf-8', sep=',', index_col = 0)
    # Entropy(data, "play")
    Gain(data,"outlook")
if __name__ == "__main__":
    main()
