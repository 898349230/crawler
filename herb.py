# encoding=utf-8
import requests
import json
import xlwt

# excel 保存路径
# excelPath = "‪C:\\Users\\89834\\Desktop\\1.xls"
excelPath2 = "2.xls"
# file = open(excelPath,'w')

# 要查询的 名称
ingredient_name_list =('artemisinin','Betea-Cubebene')
# 查询 ingredient 表头  MOL_id 是 Ingredient id
ingredient_title = ('MOL_id','Molecule_name','Molecule_formula','Molecule_weight','OB_score','PubChem_id''CAS_id',)
# 查询 ingredient url
# data={"page_size":15,"page_num":1,'table_name':'Gene'}
ingredient_url = 'http://www.symmap.org/search/'

# display 筛选条件  Gene 是 Target
related_display_table = ('Herb','TCM_symptom','MM_symptom','Gene','Disease')
# data={'rrid':'SMIT08863','table_name':'Gene','filter':0}
related_display_url = 'http://www.symmap.org/related_components/'
# Gene_id 是 target id
related_display_target_title = ('Gene_id','Gene_symbol','Chromosome','Gene_name','Protein_name','Ensembl_id','UniProt_id')


''' 没用的 '''
# Gene_id 是 Target id
targetTuple = ('Gene_id','Gene_symbol','Chromosome','Gene_name','Protein_name','Ensembl_id','UniProt_id')
# data={"table_name":"Mol","key":"artemisinin"}
targetUrl = 'http://www.symmap.org/browse/'

# 获取 ingredient id 集合
def get_ingredient_id(url,ingredient,title='MOL_id'):
    data = {"table_name": "Mol", "key": ingredient}
    response = requests.post(url, data)
    if response.status_code == 200:
        text = response.text
        dataArr = json.loads(text)['data']  # type:list
        ingredientIdList = []
        for i, data in enumerate(dataArr):
            ingredientIdList.append(dataArr[i][title])
        #         print(title, ' : ', dataArr[i][title])
        return ingredientIdList

def get_relate_target(url, id, table_name='Gene'):
    data = {'rrid': id, 'table_name': table_name, 'filter': 0}
    response = requests.post(url, data)
    if response.status_code == 200:
        text = response.text
        jsonStr = json.loads(text)
        dataArr = jsonStr['data']
        columns = jsonStr['columns']
        dictAndList = {}
        field2title = {}
        for column in columns:
            field2title.setdefault(column['field'],column['title'])
        # print("dataArr ",dataArr)
        relateList = []
        for i,data in enumerate(dataArr):
            relateDict = {}
            for field in field2title:
                # relateDict.update(title=dataArr[i][title])
                relateDict.setdefault(field,dataArr[i][field])
                # print(title, "->",dataArr[i][title], end='\t\t\t')
            relateList.append(relateDict)
        dictAndList.setdefault('data',relateList)
        dictAndList.setdefault('columns',field2title)
        return dictAndList

def export_excel(data):
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
            relateColumnDict = relateTargetDataDict['columns']
            for i, field in enumerate(relateColumnDict):
                workSheet.write(rowNum, i, relateColumnDict[field],titleStyle)
            # 遍历每条数据
            relateTargetList = relateTargetDataDict['data']
            for relateTarget in relateTargetList:
                rowNum = rowNum + 1
                colNum = 0
                for title in related_display_target_title:
                    workSheet.write(rowNum, colNum, relateTarget[title])
                    colNum = colNum + 1
            rowNum = rowNum + 1
    workbook.save(excelPath2)
    print('success')

def get_relate_target2(url, id, table_name='Gene'):
    data = {'rrid': id, 'table_name': table_name, 'filter': 0}
    response = requests.post(url, data)
    if response.status_code == 200:
        text = response.text
        jsonStr = json.loads(text)
        dataArr = jsonStr['data']
        # print("dataArr ",dataArr)
        relateList = []
        for i,data in enumerate(dataArr):
            relateDict = {}
            for title in related_display_target_title:
                # relateDict.update(title=dataArr[i][title])
                relateDict.setdefault(title,dataArr[i][title])
                # print(title, "->",dataArr[i][title], end='\t\t\t')
            relateList.append(relateDict)
        return relateList

def print_data(data):
    for ingredientName in data:
        print('ingredientName ',ingredientName)
        relateDict = data[ingredientName]
        for relateIngredientId in relateDict:
            print("relateIngredientId ", relateIngredientId)
            relateTargetList = relateDict[relateIngredientId]
            for relateTarget in relateTargetList:
                for title in related_display_target_title:
                    print(title,':', relateTarget[title],end='\t\t')
                print('')

def export_excel2(data):
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
            relateTargetList = relateDict[relateIngredientId]
            # 表头
            for i, title in enumerate(related_display_target_title):
                workSheet.write(rowNum, i, title,titleStyle)
            # 遍历每条数据
            for relateTarget in relateTargetList:
                rowNum = rowNum + 1
                colNum = 0
                for title in related_display_target_title:
                    workSheet.write(rowNum, colNum, relateTarget[title])
                    colNum = colNum + 1
            rowNum = rowNum + 1
    workbook.save(excelPath2)
    print('success')

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
    # 遍历成分名称集合
    for ingredientName in ingredient_name_list:
        ingredientId2RelateData = {}
        # 成分名称的id
        ingredientIdList = get_ingredient_id(ingredient_url,ingredientName)
        # 关联成分的靶点信息
        for ingredientId in ingredientIdList:
            if ingredientId:
                dictAndList = get_relate_target(related_display_url,ingredientId)
                ingredientId2RelateData.setdefault(ingredientId,dictAndList)
        name2dataDict.setdefault(ingredientName,ingredientId2RelateData)
    # print_data(name2dataDict)
    export_excel(name2dataDict)
