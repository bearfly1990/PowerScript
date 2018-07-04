# MessageGenerator
## 背景(Background)
我们拥有METLIFE的数据库，需要添加有意义的数据以供别的组开发和测试，在数量上也要按照要求来。\
同事已经做好了前期的分析工作，数据需求已知，主要根据她提供的一条模板message，来生成需要的数量。\
从需求上来说很简单，比如就是要把一条数据copy n份，每行的数据中的指定数据依次增长就可以了，但还是花了些时间让代码和生成方式更简洁和易配置。

## 数据分析(Data Analysis)
### Message
Import使用的模板Message是以JSON的格式存储，可以通过命令行的形式将包含message的文件加载进数据库。\
在这过程中，需要本机的资源进行计算、关联，然后再执行数据库插入的操作。\
这次需要生成的一共有`31`种不同的Message，有些比较类似，但数据结构还是不一样得。\
```json
xxxxxx
```
所以，我将所有的模板存放在一个文件夹中，程序最开始便是从这边将数据读取进去，以供后续操作。
### 数据依赖关系(Data Dependency(
有些Message导入时是有依赖关系的，有固定的导入顺序，而后面的数据需要前面先生成，在业务逻辑上才成立。\
不过，主体上以`PropertyID` `SecurityID`等几个主要的字段为变化量，以自增的方式可以推导出来。

## 项目结构(Project Structure)
之前有使用Java对Json数据处理的经验，所以直接选择使用Java来编写。\
还是使用Maven来对Jar包进行管理，主要使用到JackSon，jsonschema2pojo-maven-plugin 等处理JSON。\
日志方面还是使用`Log4j 2.x`。
## 主要的一些代码点(Main Code)

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
```java
package org.bearfly.worktools.message.models.balances;
/* import... */
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
    "msgtype",
    "msgbody"
})
public class MessageBalances extends MessageBase{
    @JsonProperty("msgtype")
    private String msgtype;
    @JsonProperty("msgbody")
    private Msgbody msgbody;
    @JsonIgnore
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /*
    get/set...
    */

}

```
#### MessageBase
在上面的JSON POJO，细心的话可以发现这些类是继承一个类`MessageBase`的。\
这个额外的类其实是我在开发的过程过发现需要一个地方存储原始的json string,没有合适的地方。\
第一个想到的就是创建一个基类来存放这个信息，也方便后续拓展。
```Java
package org.bearfly.worktools.message.models;

import com.fasterxml.jackson.annotation.JsonIgnore;

public class MessageBase {
    @JsonIgnore
    private String orgJSON;
    /*
        get/set...
    */
}
```
#### MessageKeys
此外还有一个比较重要的类便是`MessageKeys`。\
就像上文中说到，每条Message都只有几个字段需要变化，其他的保持不变，所以就用这个类来存储。
```Java
package org.bearfly.worktools.message.models;

public class MessageKeys {
    private String secIDValue;
    private Integer port;
    private Integer collateralPropertyID;
    private String collateralPropertyName;
    public MessageKeys() {
        
    }
    public MessageKeys(String secIDValue) {
        super();
        this.secIDValue = secIDValue;
    }
    public MessageKeys(String secIDValue, Integer port) {
        super();
        this.secIDValue = secIDValue;
        this.port = port;
    }

    public MessageKeys(String secIDValue, Integer port, Integer collateralPropertyID) {
        super();
        this.secIDValue = secIDValue;
        this.port = port;
        this.collateralPropertyID = collateralPropertyID;
    }
    /*
        get/set...
    */
}
```
#### MessageGenerator
`MessageGenerator`是其它对应MessageGenerator的基类，也是一个虚类，因为有abstract的方法需要各个对应不同Message的子类去实现。
同时，一些公共的变量，数据都存储在这。
```java
public abstract class MsgGenerator<E extends MessageBase> {
    private static final Logger logger = LogManager.getLogger(MsgGenerator.class);
    protected String sampleFilePath;
    protected String outputFilePath;
    protected String outputDir;
    protected Integer[] ports = { xxx, xxx, xxx};
    protected Integer[] ports_s = { xxx, xxx, xxx, xxx};

    protected Integer[] collateralRange = MsgGTRConfig.getCollateralRangeArray();

    protected Integer repeat = 3375;

    protected String[] securityIDValues = MsgGTRConfig.getSecurityIDValuesArray();
    protected String[] securityIDvaluesWithS = MsgGTRConfig.getSecurityIDValuesWithSArray();

    protected final String SUFFIX_TXT = ".txt";
    protected MsgAnalysis<E> msgAlys;
    protected Integer[] range = { 0, 1 };

    public void initRange(Integer from, Integer to) {
        range[0] = from;
        range[1] = to;
    }
    /*略...*/
```
下面这个就是我提到的需要实现的虚类，用来构造真正生成的message:
```java
public abstract void createMsg(E msg, MessageKeys mks);
```
而核心的Generate代码便是如下（可以看到用到了`createMsg`）：
```java
protected void generateToFile(final Integer secFlag, final List<MessageKeys> msgKeysList, final Integer fileNums)
        throws IOException {

    Thread thread = new Thread(new Runnable() {
        @Override
        public void run() {
            try {
                generateMsgsToFile(secFlag, msgKeysList, fileNums);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    });
    thread.start();

}
 protected void generateMsgsToFile(Integer secFlag,  List<MessageKeys> msgKeysList,  Integer fileNums) throws IOException {
        logger.debug("<---------START--------->");
        logger.debug("Sample Message File:{}", sampleFilePath);
        E msg = msgAlys.getSampleMessage();
        Integer numsEachFile = 0;
        //Integer numsLastFile = 0;
        if(msgKeysList.size() % fileNums == 0) {
            numsEachFile = msgKeysList.size() / fileNums;
        }else {
            numsEachFile = msgKeysList.size() / fileNums + 1;
            //numsLastFile = msgKeysList.size() - numsEachFile * (fileNums - 1);
        }
        
        logger.debug("Total File Nums:{}, Total Json Nums:{}", fileNums, msgKeysList.size());
        for (Integer k = 1; k <= fileNums; k++) {
            String tempOFP = outputFilePath.replaceAll("%siv", securityIDValues[secFlag]);
            if (fileNums == 1) {
                tempOFP = String.format("%s_%s%s", tempOFP, "ALL", SUFFIX_TXT);

            } else {
                tempOFP = String.format("%s_%s%s", tempOFP, k.toString(), SUFFIX_TXT);
            }

            FileUtils.createDirectory(FileUtils.getDirFromFullPath(tempOFP));

            logger.debug("Create FileDir:{}", FileUtils.getDirFromFullPath(tempOFP));
            logger.debug("Create FileName:{}", FileUtils.getFileNameFromFullPath(tempOFP));
            
            try (FileWriter fw = new FileWriter(tempOFP);
                    BufferedWriter bw = new BufferedWriter(fw);
                    PrintWriter out = new PrintWriter(bw)) {
                for (Integer i = (k - 1) * numsEachFile; i < k * numsEachFile; i++) {
                    if(i < msgKeysList.size()) {
                        createMsg(msg, msgKeysList.get(i));
                        out.println(JSONUtils.getJSONFromObj(msg));
                    }
                }

            }
            logger.info("Created FileName:{}", tempOFP);
        }
        logger.debug("<=========ENDED=========>");

    }
```
#### msgKeysList
可以看到，generate的时候不关注到底是什么类型的message，只需要你提供msgKeysList就可以了，而这个数据是怎么产生的呢，举个栗子:smile:
像这个Message就比较特殊，他有自己的生成规则，所以他只需要构造好自己的`msgKeysList`，实现`createMsg`方法，之后调用父类的`generateToFile`方法就成了。
```java
    public void generate_5400_1(Integer secFlag, Integer fileNums) throws IOException {
        repeat = 3375;
        ports = new Integer[] { 13244, 13247 };
        ArrayList<MessageKeys> msgKeysList = new ArrayList<MessageKeys>();
        for (int i = 0; i < repeat; i++) {
            for (int j = 0; j < ports.length; j++) {
                if (ports[j] == 13247 && (j * repeat + i) > 5399) {
                    continue;
                }
                Integer num = (j * repeat + i);
                msgKeysList.add(new MessageKeys(securityIDValues[secFlag] + num.toString(), ports[j]));
            }
        }
        generateToFile(secFlag, msgKeysList, fileNums);

    }
    @Override
    public void createMsg(MessageBalances msg, MessageKeys mks) {
        msg.getMsgbody().getMTGBALPORTALLOC().get(0).setPortfolio(mks.getPort());
        msg.getMsgbody().getSECID().setSecurityIDValue(mks.getSecIDValue());
    }
```
#### MessageAnalysis
在每个Generator构建的时候，其实会利用MessageAnalysis对象去读取模板Message。不过话说回来，现在想想，这个类不是必须，完全可以整合到`MessageGenerator`类中
```java
package org.bearfly.worktools.message;
/* import...*/
public class MsgAnalysis<E extends MessageBase> {
    private static final Logger logger = LogManager.getLogger(MsgAnalysis.class);
    private Queue<E> msgQueue = new LinkedList<>();
    private JsonProvider jsonProvider = Configuration.defaultConfiguration().jsonProvider();
    public MsgAnalysis() {

    }

    public MsgAnalysis(String msgFilePath, Class<E> clazz) throws IOException {
        readMessages(msgFilePath, clazz);
    }

    public void readMessages(String msgFilePath, Class<E> clazz) throws IOException {
        List<String> lines = FileUtils.readTextFile(msgFilePath);
        msgQueue = new LinkedList<>();
        for (String line : lines) {
            if(line.trim().equals(""))continue;
            @SuppressWarnings("unchecked")
            E msg =  (E) JSONUtils.getObjFromJSON(line, clazz);
            msg.setOrgJSON(line);
           
            logger.debug(msg.getOrgJSON());
            msgQueue.add(msg);
        }
        
        for(int i = 0 ; i< 100; i++) {
            @SuppressWarnings("unchecked")
            E msg =  (E) JSONUtils.getObjFromJSON(msgQueue.peek().getOrgJSON(), clazz);
            msgQueue.add(msg);
        }
    }
  /*get/set...*/
}

```
```java
public AdvanceGenerator(String sampleFilePath, String outputFilePath) throws IOException {
    super(sampleFilePath, outputFilePath);
    msgAlys = new MsgAnalysis<MessageBalances>(sampleFilePath, MessageBalances.class);
}

```
### MessageFactory
工厂类去创建对象和调用生成代码，创建顺序，生成文件的数目目前都hardcode在这边

### 配置文件(Config File To Generate Expected Records)
将项目打包成jar包之后，可以通过配置文件有限的复用。\
如下所示，最重要的是`generateFlags`，这个数组标志对应上面的不同变量，并可以指定生成哪些。
```properties
sampleJsonDir=xxx\\SampleMessages\\
outputDir=xxx\\WorkFlow_CX
collateralRange=2,60001,120001,180001,240001
securityIDValues=WKLMF,XKLMF,YKLMF,ZKLMF,AKLMF
securityIDvaluesWithS=WKLMFS,XKLMFS,YKLMFS,ZKLMFS,AKLMFS
generateFlags=0,1,2,3
```
