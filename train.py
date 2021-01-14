import copy
import re


# toutiao_cat_data.txt中的数据包含大量非汉字字符，以下过滤器可以剔除非汉字成分
def get_main(string):
    string = re.sub("[A-Za-z0-9\%\[\]\《\》\“\”\//\」\「\…\(.-.)\│\-\（\）\'\"\’\:\：]", "", string.strip())
    return string.split('_!_')[3:]


# 读取训练数据，对数据去噪（只保留能够分隔句子的标点符号），最后以句为单位存入列表
def load_data():
    list = []
    with open('src/toutiao_cat_data.txt', errors='ignore') as f:
        line = f.readline()
        while line:
            line=get_main(line)
            for i in line:
                list += re.split('[\？\，\！\.\-\；\/\·\—\―\（\）\~\|\~\&\？\(\)\?\→\Ⅱ\｜\─\㎡\│\、\,]', i)
            line = f.readline()
    return list


# 对列表中的每个纯中文句子遍历，以前一个字、后一个字为键，次数为值构建二维字典
# 如”意思意思”对应列表{‘意’：{’思‘：2}，’思‘：{’意‘：1}}
def train1(lis):
    train = {}
    for str in lis:
        if len(str) > 1:
            for j in range(len(str) - 1):
                if str[j] not in train.keys():
                    train[str[j]] = {}
                    if str[j + 1] not in train[str[j]].keys():
                        train[str[j]][str[j + 1]] = 1
                elif str[j + 1] not in train[str[j]].keys():
                    train[str[j]][str[j + 1]] = 1
                else:
                    train[str[j]][str[j + 1]] += 1
    return train


# 二次处理，将train1返回的字典中的次数替换为前字下后字出现的概率
def HMM(dic):
    probability = copy.deepcopy(dic)
    probability['none']={}
    for d in dic.keys():
        t = dic[d]
        num = sum(t.values())
        for i in t.keys():
            probability[d][i] = t[i] / num
        probability[d]['none']=1/num/1000000000
        probability['none'][d]=1/num/1000000000
    return probability


# 汇总训练过程，方便调用
def get_train():
    return HMM(train1(load_data()))


if __name__ == '__main__':
    #查看处理后的语料
    data=load_data()
    print(data)
    #查看状态转移概率
    print(get_train())