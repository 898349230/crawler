# encoding=utf-8
import requests
import json
import xlwt
import xlrd

# excel 保存路径 要保存成‘xls’ 格式 不要保存 ‘xlsx’
exportExcelPath = "C:\\Users\\89834\\Desktop\\herb.xls"
# 读取的 excel 地址
sourceExcelPath = 'C:\\Users\\89834\\Desktop\\成分1.xlsx'

# 要查询的 名称
ingredient_name_list =('"1,8-Cineole"','Betea-Cubebene')

# 查询 ingredient 表头  MOL_id 是 Ingredient id
ingredient_title = ('MOL_id','Molecule_name','Molecule_formula','Molecule_weight','OB_score','PubChem_id''CAS_id')
# 查询 ingredient url
# data={"page_size":15,"page_num":1,'table_name':'Gene'}
ingredient_url = 'http://www.symmap.org/search/'

# display 筛选条件  Gene 是 Target
related_display_table = ('Herb','TCM_symptom','MM_symptom','Gene','Disease')
# data={'rrid':'SMIT08863','table_name':'Gene','filter':0}
related_display_url = 'http://www.symmap.org/related_components/'
# Gene_id 是 target id
related_display_target_title = ('Gene_id','Gene_symbol','Chromosome','Gene_name','Protein_name','Ensembl_id','UniProt_id')

''' 获取 ingredient id 集合 '''
def get_ingredient_id(url,ingredient,title='MOL_id'):
    data = {"table_name": "Mol", "key": ingredient}
    response = requests.post(url, data,timeout=5)
    if response.status_code == 200:
        text = response.text
        dataArr = json.loads(text)['data']  # type:list
        ingredientIdList = []
        for i, data in enumerate(dataArr):
            ingredientIdList.append(dataArr[i][title])
        #         print(title, ' : ', dataArr[i][title])
        return ingredientIdList

''' 
根据 ingredient_id 获取相关数据
display 筛选条件  Gene 是 Target
table_name 可选值： 'Herb','TCM_symptom','MM_symptom','Gene','Disease'
'''
def get_relate_target(url, id, table_name='Gene'):
    data = {'rrid': id, 'table_name': table_name, 'filter': 0}
    response = requests.post(url, data)
    print("抓取 ingredientId:",id)
    if response.status_code == 200:
        text = response.text
        jsonStr = json.loads(text)
        dataArr = jsonStr['data']
        columns = jsonStr['columns']
        dataDict = {}
        field2title = {}
        titleList = []
        # 表头与返回数据key的对应关系
        for column in columns:
            field2title.setdefault(column['field'],column['title'])
            titleList.append(column['title'])
        # print("dataArr ",dataArr)
        relateList = []
        for i,data in enumerate(dataArr):
            relateDict = {}
            for field in field2title:
                # relateDict.update(title=dataArr[i][title])
                relateDict.setdefault(field2title[field],dataArr[i][field])
                print(field2title[field], ":",dataArr[i][field], end='\t\t')
            relateList.append(relateDict)
            print()
        dataDict.setdefault('data',relateList)
        dataDict.setdefault('titleList',titleList)
        return dataDict

'''
读取excel中第一列的内容
'''
def read_excel(sourceExcelPath):
    workBook = xlrd.open_workbook(sourceExcelPath) # type:xlrd.Book
    first_sheet = workBook.sheet_by_index(0)
    valueList = first_sheet.col_values(0)
    return valueList

'''
导出excel
'''
def export_excel(data, exportPath):
    workbook = xlwt.Workbook(encoding='utf-8')
    workSheet = workbook.add_sheet("ingredient") # type:xlwt.Worksheet
    # 颜色
    nameStyle = cellColourStyle(2)
    idStyle = cellColourStyle(3)
    titleStyle = cellColourStyle(22)
    rowNum = 0
    for ingredientName in data:
        workSheet.write(rowNum,0,ingredientName,nameStyle)
        rowNum = rowNum + 1
        # 成分名称对应的数据
        relateDict = data[ingredientName]
        # 一个成分对应多个 IngredientId
        for relateIngredientId in relateDict:
            workSheet.write(rowNum, 0, relateIngredientId,idStyle)
            rowNum = rowNum + 1
            # 每个 relateIngredientId 对应的一组数据
            relateTargetDataDict = relateDict[relateIngredientId]
            # 表头
            titleList = relateTargetDataDict['titleList']
            for i,title in enumerate(titleList):
                workSheet.write(rowNum, i, title, titleStyle)
            # 遍历每条数据
            relateTargetList = relateTargetDataDict['data']
            for relateTarget in relateTargetList:
                rowNum = rowNum + 1
                colNum = 0
                for title in titleList:
                    workSheet.write(rowNum, colNum, relateTarget[title])
                    colNum = colNum + 1
            rowNum = rowNum + 1

    workbook.save(exportPath)
    print('导出成功，文件为：', exportPath)

''' 打印数据 测试用 '''
def print_data(data):
    for ingredientName in data:
        print('ingredientName ',ingredientName)
        relateDict = data[ingredientName]
        for relateIngredientId in relateDict:
            print("relateIngredientId ", relateIngredientId)
            relateTargetDataDict = relateDict[relateIngredientId]
            # 表头
            titleList = relateTargetDataDict['titleList']
            # 每条数据
            relateTargetList = relateTargetDataDict['data']
            for relateTarget in relateTargetList:
                for i,title in enumerate(titleList):
                    print(title,':', relateTarget[title],end='\t\t')
                print('')

''' excel背景色 '''
def cellColourStyle(colourNum):
    pattern = xlwt.Pattern() # type: xlwt.Pattern
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    # 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan,
    # 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown),
    # 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray
    pattern.pattern_fore_colour = colourNum
    style = xlwt.XFStyle()
    style.pattern = pattern
    return style

if __name__ == '__main__':
    name2dataDict = {}
    failNameList = []
    # 读取 excel 内的名称
    name_list = read_excel(sourceExcelPath)
    # 手动填写名称
    # name_list = ingredient_name_list
    # 遍历成分名称集合
    for ingredientName in name_list:
        if ingredientName:
            ingredientId2RelateData = {}
            # 成分名称的id
            print('开始抓取：',ingredientName,' 数据')
            try :
                ingredientIdList = get_ingredient_id(ingredient_url,ingredientName)
            except Exception as result:
                print(ingredientName,' 获取数据失败')
                failNameList.append(ingredientName)
                continue
            else:
                if ingredientIdList:
                    # 关联成分的靶点信息
                    for ingredientId in ingredientIdList:
                        if ingredientId:
                            # get_relate_target 第三个参数可以修改 根据display 选项获取不同的数据，默认是 Target
                            # display 筛选条件  Gene 是 Target
                            # table_name ： 'Herb','TCM_symptom','MM_symptom','Gene','Disease'
                            # dictAndList = get_relate_target(related_display_url,ingredientId,'TCM_symptom')
                            dictAndList = get_relate_target(related_display_url,ingredientId)
                            ingredientId2RelateData.setdefault(ingredientId,dictAndList)
                name2dataDict.setdefault(ingredientName,ingredientId2RelateData)

    # print_data(name2dataDict)
    print('准备导出数据')
    export_excel(name2dataDict, exportExcelPath)
