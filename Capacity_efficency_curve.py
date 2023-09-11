import os

import pandas as pd


def Process_Cap_Eff(src: str, out: str):
    df = pd.DataFrame(pd.read_csv(src, encoding='gbk'))


    if df.iloc[:, 1].mean() >= df.iloc[:, 0].mean():
        df['库伦效率'] = df.iloc[:, 0] / df.iloc[:, 1] * 100
    else:
        df['库伦效率'] = df.iloc[:, 1] / df.ilco[:, 0] * 100
    # 导出文件的路径为：”设置的导出目录“+”\out“（用于区别源文件）+“源文件名”（包含文件后缀）
    df.to_csv(out + r"\out_" + os.path.basename(src), encoding='gbk')


if __name__ == '__main__':
    # 原数据文件地址
    url = r'C:\Users\77277\Desktop\效率.csv'

    # 文件输出地址
    url2 = r'C:\Users\77277\Desktop\result2.csv'
    Process_Cap_Eff(url, url2)
