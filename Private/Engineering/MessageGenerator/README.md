# MessageGenerator
## 背景(Background)
我们拥有METLIFE的数据库，需要添加有意义的数据以供别的组开发和测试，在数量上也要按照要求来。\
同事已经做好了前期的分析工作，已知主要的数据需求，我介入时主要根据她提供的一条模板message，来生成需要的数量。\
从需求上来说很简单，比如就是要把一条数据copy n份，每行的数据中的指定数据依次增长就可以了，但还是花了些时间让代码和生成方式更简洁和易配置。

## 数据分析(Data Analysis)
### Message
Import使用的模板Message是以JSON的格式存储，可以通过命令行的形式将包含message的文件加载进数据库。\
在这过程中，需要本机的资源进行计算、关联，然后再执行数据库插入的操作。\
这次需要生成的一共有`31`种不同的Message，有些比较类似，但数据结构还是不一样得。\
```json
{"msgtype":"COLLATERALAPPRAISALS","msgbody":[{"Operation":"ADD","PropertyID":55000,"ReportEffectiveDate":20171231,"AppraisalDate":20171231,"AppraiserID":0,"PriceIndexID":0,"LandValue":456200,"IncomeValue":563200,"OpinionValue":12300,"ScheduleBValue":65800,"InsurableAmount":754000,"CostValue":700000,"IncomeCapRate":15,"MarketValue":870000,"ReplacementCost":256300,"Occupancy":65}]}
```
所以，我将所有的模板存放在一个文件夹中，程序最开始便是从这边将数据读取进去，以供后续操作。
### 数据依赖关系 Data Dependency
有些Message导入时是有依赖关系的，有固定的导入顺序，而后面的数据需要前面先生成，在业务逻辑上才成立。\
不过，主体上以`PropertyID``SecurityID`等几个主要的字段为变化量，以自增的方式可以推导出来。

## Project Structure
之前有使用Java对Json数据处理的经验，所以直接选择使用Java来编写。\
还是使用Maven来对Jar包进行管理，主要使用到JackSon，jsonschema2pojo-maven-plugin 等处理JSON。\
日志方面还是使用`Log4j 2.x`。
## Main Code

### Json <=> Object
上面提到了JackSon和jsonschema2pojo-maven-plugin,对JSON的处理完全是靠他们来完成了。
#### JackSon
JackSon算是比较流行的JSON处理库，使用起来也很方便e.g.
```Java
ObjectMapper mapper = new ObjectMapper();
Object obj = mapper.readValue(jsonStr, clazz);
String jsonInString = mapper.writeValueAsString(obj);
```
而在使用JackSon之前，那就是需要有对应的Object类，这样才能把clazz传进去。这时候就需要用到jsonschema2pojo-maven-plugin。
#### jsonschema2pojo-maven-plugin
```xml
<plugin>
    <groupId>org.jsonschema2pojo</groupId>
    <artifactId>jsonschema2pojo-maven-plugin</artifactId>
    <version>0.5.1</version>
    <configuration>
        <sourceDirectory>${basedir}/src/main/resources/json</sourceDirectory>
        <sourceType>json</sourceType>
        <targetPackage>org.bearfly.worktools.message.models.fundnewloan</targetPackage>
    </configuration>
    <executions>
        <execution>
            <goals>
                <goal>generate</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```
在`pom.xml`中加入以上配置，那么执行 `mvn package`的时候，它会自动将resources下的json文件生成对应的POJO类。\
可以在`build\java-gen`目录下找到生成的类。
### MessageGenerator

### MessageFactory

### MultiThread To Generate Files

### 控制生成文件数量的逻辑(Control File Numbers)

### Config File To Generate Expected Records
