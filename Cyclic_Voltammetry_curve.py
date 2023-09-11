from copy import deepcopy
import os

import pandas as pd


def Process_CV(src: str, out: str):
    # 读取txt 文件，以 , 为分隔符.  注意：txt导入时，默认所有数据为str 格式
    df = pd.DataFrame(pd.read_table(src, header=None, sep=',', encoding='gbk'))

    # 创建字典收集相关信息
    info = {}

    info.update({'Date': df.loc[0, 0] + df.loc[0, 1]})  # 保存日期信息
    info.update({df.loc[2, 0].split(':', 1)[0]: df.loc[2, 0].split(':', 1)[1]})  # 保存文件路径信息
    info.update({df.loc[4, 0].split(':')[0]: df.loc[4, 0].split(':')[1]})  # 保存实验设备信息

    # 循环保存初始电压、最高电压、最低电压、初始充放电、扫描速率、分段数、扫描间隔等
    for x in range(9):
        info.update({df.loc[x + 7, 0].split('=')[0]: df.loc[x + 7, 0].split('=')[1]})

    # 打印保存的信息
    for x in info.keys():
        print(x, info[x], end='\n')

    # 创建列表用于保存各段数据
    contain = []

    # 循环读取数据
    flag = df.shape[0]
    for x, y in df.iterrows():
        if y[0] == 'Potential/V': flag = x + 1  # 读取到'Potential/V' 时，激活flag 正式开始处理数据
        if x >= flag:
            if float(y[0]) == float(info['High E (V) ']):  # txt 文件导入时，默认所有类型都是str，需要手动将数据转化为float
                temp = deepcopy(df[flag: x + 1])
                contain.append(deepcopy(df[flag: x + 1]))
                flag = x

    # 如果原数据最后没有以 High E (V) 结尾，手动补上最后一组数据
    if df.tail(1).iloc[0, 0] != info['High E (V) ']:
        contain.append(deepcopy(df[flag: df.shape[0]]))
    del flag

    # 创建result 用于储存处理好的数据
    result = pd.DataFrame()

    #
    flag = 0
    for x in contain:
        flag += 1
        x.reset_index(drop=True, inplace=True)
        x.columns = ['第{}轮放电'.format(flag), '第{}轮充电'.format(flag)]
        result = pd.concat([result, x], axis=1, ignore_index=True)  # 此处ignore_index=True，忽视原有的索引，防止新增列堆叠在元数据后

    # 打印并导出处理后数据
    print(result)
    # # 导出文件的路径为：”设置的导出目录“+”\out“（用于区别源文件）+“源文件名”（包含文件后缀）
    result.to_csv(out + r"\out_" + os.path.basename(src), encoding='gbk')


if __name__ == '__main__':
    # 原数据文件路径
    url = r'C:\Users\77277\Desktop\效率.txt'
    # 导出数据文件路径
    url2 = r'C:\Users\77277\Desktop\result3.csv'
    Process_CV(url, url2)
