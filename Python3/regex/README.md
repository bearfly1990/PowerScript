---
layout:     post
title:      Regex in python
subtitle:   Simple introduce of using regex in python
date:       2018-05-07
author:     BF
header-img: img/post-bg-kuaidi.jpg
catalog: true
tags:
    - python
    - regex
---
## Regex in python 简介
[正则表达式](https://en.wikipedia.org/wiki/Regular_expression) 是在文本处理的时候非常高效有用的一种方式，一般的编程语言都会内置相应的模块。

不同的编程语言使用方式不尽相同，核心的表达式模式都是一致的。

最近使用python生成Message，有用到正则表达式，今天简单的总结下python使用的方式。对于表达式本身的使用，之后有时间再详细介绍。

### re.match
首先介绍下`re.match(pattern, string, flags=0)`。

如果能匹配上，这个方法将会返回match对象, 如果失败的话就会返回None。

看下面这个例子，我在创建message的时候，希望通过配置类似于`Suffix[1-100]`这样的方式来生成message中的变量。我需要得到前缀`Suffix`,最小值`1`,最大值`100`。
```python
import re

line = "Suffix[1-100]"

matchObj = re.match( r'(.*)\[(.*?)-(.*?)\]', line, re.M|re.I)

if matchObj:
   print ("matchObj.group() : ", matchObj.group())
   print ("matchObj.group(1) : ", matchObj.group(1))
   print ("matchObj.group(2) : ", matchObj.group(2))
   print ("matchObj.group(3) : ", matchObj.group(3))
else:
   print ("No match!!")
'''output
matchObj.group() :  Suffix[1-100]
matchObj.group(1) :  Suffix
matchObj.group(2) :  1
matchObj.group(3) :  100
'''
```
通过`match`方法，利用`group()`就能很方便的把固定格式的数据提取出来。

### re.search
在字符串中利用正则表达式查找匹配相可以使用`re.search(pattern, string, flags=0)`

那么`search`和`match`有什么区别呢？

其实从名字上就可以看出来，`search`是在整个字符串里找符合匹配的就可以，而`match`要求整个字符串来匹配。
```python 
import re
line = "Cats are smarter than dogs, but I like dogs:) ";

matchObj = re.match( r'dogs', line, re.M|re.I)
if matchObj:
   print ("match --> matchObj.group() : ", matchObj.group())
else:
   print ("No match!!")

searchObj = re.search( r'dogs', line, re.M|re.I)
if searchObj:
   print ("search --> searchObj.group() : ", searchObj.group())
else:
   print ("Nothing found!!")
```

### re.sub
`re.sub(pattern, repl, string, max=0)`用来查找和替换字符串。`max`是可选的，表示替换的个数，默认是全部替换。


```python 
import re

phone = "2004-959-559 # This is Phone Number"

# Delete Python-style comments
num = re.sub(r'#.*$', "", phone)
print "Phone Num : ", num

# Remove anything other than digits
num = re.sub(r'\D', "", phone)    
print "Phone Num : ", num
```

### string
就像其它编程语言一样，python中`string`已经内置了一些和文本有关的方法，可以直接方便使用。
`s.startswith(prefix[,start[,end]])`
`s.endswith(suffix[,start[,end]])`
`s.find(sub[,start[,end]])`
`s.split([sep])`
...

### Flags
上面的例子中，大家发现了又用到`re.M|re.I`,这些常量是用来定义匹配模式的，

| Sr.No.   |      Modifier | Description          |
|----------|:-------------:|----------------------|
| 1        |  re.I         | 大小写敏感              |
| 2        |  re.L         | 使用Local,影响`\W` `\w`和`\B` `\b`|
| 3        |  re.M         | ^匹配行结尾  $匹配行开头  |
| 4        |  re.S         | 让`.`匹配任何字符，包括换行 |
| 5        |  re.U         | 使用Unicode编码 影响`\W` `\w`和`\B` `\b` |
| 6        |  re.X         | 允许`cuter`语法，忽略空白(在[]或者\）,并将#做为一般正常字符|


更具体的信息参考：[Python - Regular Expressions](https://www.tutorialspoint.com/python/python_reg_expressions.htm)
