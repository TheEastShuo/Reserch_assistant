from copy import deepcopy
import os

import pandas as pd


def Process_Cap_Volt(src: str, out: str):
    # 打开csv文件，以gbk方式解码，实现中文的识别
    df = pd.DataFrame(pd.read_csv(src, encoding='gbk'))

    # 第一次循环删去电池静置时间
    for x, y in df.iterrows():
        print(y.tolist()[0])
        if y.tolist()[0] == 0:
            df.drop(x, inplace=True)
        else:
            break
    df.reset_index(drop=True, inplace=True)

    # 用列表分段储存电池循环数据
    contain = list()

    # 以比容量为0作为分段依据，将源数据分段储存到列表中
    flag = 0
    for x, y in df.iterrows():
        if y.tolist()[0] == 0:
            contain.append(deepcopy(df.loc[flag:x - 1]))  # 此处采用深拷贝，防止df的修改引起变化
            flag = x
        else:
            pass
    print(flag)

    # 手动补充最后一段充/放电顺序
    contain.append(deepcopy(df.loc[flag:df.shape[0]]))
    del flag
    del df

    # 打印储存各段充/放电数据
    print(contain)

    # 新建DataFrame对象，将列表中各段充/放电数据按列存入其中
    result = pd.DataFrame()

    # 迭代读取列表中分段储存的实验数据
    flag = 0
    for x in contain:
        temp = x
        temp.reset_index(drop= True, inplace=True)
        temp.columns = ['第{}轮比容量'.format(flag + 1), '第{}轮电压'.format(flag + 1)]
        result = pd.concat([result, temp], axis=1, ignore_index=False)  # 此处ignore_index=True，忽视原有的索引，防止新增列堆叠在元数据后
        flag += 1
    else:
        del flag

    # 重新设置数据索引
   # result.reset_index(drop=True, inplace=True)

    # 打印并导出处理后的数据
    print(result)
    # 导出文件的路径为：”设置的导出目录“+”\out“（用于区别源文件）+“源文件名”（包含文件后缀）
    result.to_csv(out + r"\out_" + os.path.basename(src), encoding='gbk')


if __name__ == '__main__':
    # 源数据文件路径
    url = r'C:\Users\77277\Desktop\比容量-电压.csv'
    # 导出的数据文件路径
    url_end = r'C:\Users\77277\Desktop\result.csv'
    Process_Cap_Volt(url, url_end)