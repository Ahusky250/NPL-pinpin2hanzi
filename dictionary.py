def make_dic():
    direction={}
    with open('src/pinyin2hanzi.txt') as f:
        line=f.readline()
        while line:
            a=line.strip().split(' ')
            # print(a)
            direction[a[0]]=a[1]
            line=f.readline()
    return direction


if __name__=='__main__':
    #查看导入的字典
    print(make_dic())