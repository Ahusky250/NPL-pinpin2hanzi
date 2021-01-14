import dictionary
import train


# 提取拼音序列
def get_pinyin():
    pinyin = []
    with open('src/测试集.txt') as f:
        line = f.readline()
        while line:
            pinyin.append(line.split())
            f.readline()
            line = f.readline()
    return pinyin


# 提取正确汉语
def get_ideal_answer():
    ideal_answer = []
    with open('src/测试集.txt') as f:
        line = f.readline()
        while line:
            line = f.readline()
            ideal_answer.append(line.strip())
            line = f.readline()
    return ideal_answer


# 维比特算法实现拼音向汉语的转化
def viterbi(lis, dic, train):
    hanyu = ''
    most_probability = 0
    hanzi_list = [dic[i.lower()] for i in lis]
    head = hanzi_list[0]
    hanzi_list = hanzi_list[1:]
    for head_zi in head:
        temp = head_zi
        before_zi = head_zi
        tp = 1
        for after in hanzi_list:
            # this_zi的含义为，同一个拼音下，选择的字
            this_zi = ''
            max_p = 0
            # 找出最有可能出现在before_zi后的字
            for after_zi in after:
                # 训练结果中有记录前一个字为before_zi后一个字为after_zi的情况
                # print(before_zi,'   and   ',after_zi)
                if before_zi in train.keys() and after_zi in train[before_zi].keys():
                    if max_p < train[before_zi][after_zi]:
                        max_p = train[before_zi][after_zi]
                        this_zi = after_zi
                else:
                    # toutiao_cat_data.txt未包含pinyin2hanzi.txt中所有的汉字，但包含了before_zi
                    if before_zi in train.keys():
                        if max_p < train[before_zi]['none']:
                            max_p = train[before_zi]['none']
                            this_zi = after_zi
                    elif after_zi in train['none'].keys():
                        if max_p < train['none'][after_zi]:
                            max_p = train['none'][after_zi]
                            this_zi = after_zi
                    else:
                        # 最特殊的情况，两个汉字都未在训练集出现
                        pass
            before_zi = this_zi
            tp *= max_p
            temp += this_zi
            # print(this_zi,'出现的概率最大')
        if most_probability < tp:
            hanyu = temp
            most_probability = tp
        tp = 1
    return hanyu


# 句子接近程度计算，标准为同位置相同的字符的数量占句子长度的比例
def cal_acc(ideal_hanyu, train_hanyu):
    assert (len(ideal_hanyu) == len(train_hanyu))
    print('正确的句子\t\t\t', ideal_hanyu)
    print('viberti算法得到的句子\t', train_hanyu)
    num = len(ideal_hanyu)
    cnt = 0
    for i in range(num):
        if ideal_hanyu[i] == train_hanyu[i]:
            cnt = cnt + 1
    return cnt / num


# 模型评估
def assess():
    pinyin = get_pinyin()  # 保存拼音
    ideal_answer = get_ideal_answer()  # 保存正确结果
    dic = dictionary.make_dic()  # 加载字典
    train_result = train.get_train()  # 加载训练结果
    assert (len(pinyin) == len(ideal_answer))
    num = len(pinyin)
    acc_list = []  # 记录每次拼音到汉语转化的准确度
    for i in range(num):
        print('拼音为', pinyin[i])
        acc_list.append(cal_acc(ideal_answer[i], viterbi(pinyin[i], dic, train_result)))
    print('21条测试用例的平均准确率为', sum(acc_list) / num)


if __name__ == '__main__':
    assess()
