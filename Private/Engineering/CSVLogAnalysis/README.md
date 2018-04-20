## AnalyseCSVLogByMonth
基于之前的Message Import测试工具，会生成原始的log文件[TestResult.csv](TestResult.csv)。
```csv
path,rows,timeused(s),timeused(m),avgtime,messageDate
Step01,60000,270.18,4.50,0.0045,20161231
Step02,60000,197.96,3.30,0.0033,20171231
...
```
而现在又了新的需求，希望能统计一下基于月份的运行时间，所以我简单写了个python脚本，来解析csv文件，将同一个月份的数据group起来。
## 主要流程与算法
### 运行流程
```python
resultList = readCSVRowsList("TestResult.csv")
resultList = initAndSortByMessageMonth(resultList, 5)
resultList = combineRowsByColumn(resultList, 5)
writeToCSVFile("out.csv", resultList)
```
1. 将csv文件加载到二维数组中
2. 将`MessageDate`截取成yyyyMM的格式，并加入`#`，然后返回据此排序好的二维数组(List)。
   同时在代码里可以看到我还做了特殊处理，这个是具体的需求。通用的处理可以直接删除掉。
3. 将相同月份的数据Combine到一起再返回新的数组回来
4. 将最后的数据写入到输出文件[TestResultCombined.csv](estResultCombined.csv)

### 数据Combine算法
代码中我已经做了注释，不再过多解释，就是逐行处理，结果放到新的list里。
```python
def combineRowsByColumn(csvRowsList, columnIndex = 5):
    resultList = []
    for i, row in enumerate(csvRowsList):
        # keep csv header and do nothing
        if(i == 0):
            resultList.append(row)
            continue
            
        currentValue = row[columnIndex]
        # get the month of last row
        if(i - 1 >= 0):
            lastValue = csvRowsList[i-1][columnIndex]
        else:
            lastValue = None
        # get the month of next row
        if(i + 1 < len(csvRowsList)):
            nextValue = csvRowsList[i+1][columnIndex]
        else:
            nextValue = None
        # if last month is the same with current month, combine them
        if(lastValue != None and lastValue == currentValue):
            for j in range(len(row)):
                #ignore the mmonth column
                if(j == columnIndex):
                    pass
                else:
                    # if is value, calculate them, if not ,just append them with '~'
                    if(isFloat(row[j])):
                        row[j] = "{:.2f}".format(float(row[j]) + float(csvRowsList[i-1][j]))
                    else:
                        row[j] = csvRowsList[i-1][j] + "~" + row[j]
        # if next value is different, just add current row to the new list
        if(currentValue != nextValue):
                resultList.append(row)  
    return resultList    
```

