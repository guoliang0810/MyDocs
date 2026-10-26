# encoding: utf-8
import json
import csv
import xlrd


# 读取json文件
def get_json_data(path):
    #度文件：
    f = open(path,'r')
    jsondata = f.read()
    #json -> python对象
    pyobj = json.loads(jsondata)
    #字典
    datas = [pyobj['user'],pyobj['pwd']]
    return datas


# csv数据读取：
def get_csv_data(path):
    f = open(path,'r')
    reder = csv.reader(f)
    #跳过第一行：
    next(reder,None)
    row = []
    for n in reder:
        row.append(n)
    return row[0]


#操作表格
def get_xlsx_data(path):
    #路径 中文/Users/p/venv/bin/untitled/day13/my.xlsx
    # path = path.decode('utf-8')
    #打开工作区间
    data = xlrd.open_workbook(path)
    table = data.sheet_by_name('Sheet1')
    #获取行和列
    rwos = table.nrows
    cols = table.ncols
    mydd = []
    for r in range(rwos):
        for c in range(cols):
            d = table.cell_value(r,c)
            mydd.append(d)
    print(mydd)
    # [{},{},{}]
    # [[],[],[]]
    #获取第二行值：
    row_value = table.row_values(1)
    #float -> int -> str
    a = str(int(row_value[0]))
    b = str(int(row_value[1]))
    return [a,b]

# get_xlsx_data('/Users/p/venv/bin/untitled/day18/data/my.xlsx')





