## PAM Data Compare

PAM Data in BA Server is stored in the SqlServer DB, it has his own logic to store the data.
The Original PAM Data is Stored in Impala table and it's easy to get the column name and type.
### 需求分析
不知道为什么？
BA Server 将mart的信息分布在不同的几张表中，首先需要用sql把表连接起来得到数据。
sample as below：为b了解耦，我将sql语句写在了独立的文件中，通过XMLUtil来读取，进而在DAO中使用。
```sql
--query_sqlserver.xml
select 
    M.id martID, 
    M.physical_name martName,
    MV.id martVersionId,
    ME.id martElementID,
    ME.physical_name martElementName,
    ME.type martElementType,
    ME.business_view_id businessID,
    BV.display_name businessName,
    BV.isCore isCore
    from tblMartVersion MV, tblMart M, tblMartElement ME, tblBusinessView BV 
    where m.id = MV.mart_id and MV.mart_id = ME.mart_version_id 
    and ME.business_view_id = BV.id
    and M.id = %s
```
而PAM这边就比较简单，直接取得Column的名字(Name)和类型(Type)就行：
```sql
--query_impala.xml
    describe  %s
```
### 数据源配置文件
DBInfo.properties存储的是数据库的信息，由FileConfig.java读取这部分信息，并在代码中使用
```ini
impala.datasource1.url=jdbc:impala://hadoop07.dev.pr1.eexchange.com:21050/metldw595d;SSL=1;CAIssuedCertNamesMismatch=1;SSLTrustStore=C:/ProgramDev/jdk1.7.0_51_64bit/jre/lib/security/cacerts;SSLTrustStorePwd=changeit;AuthMech=1;KrbServiceName=impala;KrbAuthType=1;KrbRealm=CURNX.COM;KrbHostFQDN=hadoop07.dev.pr1.eexchange.com;

impala.datasource1.username=
impala.datasource1.password=
impala.datasource1.driverClassName=com.cloudera.impala.jdbc41.Driver


#sqlserver.datasource1.url=jdbc:sqlserver://fr1xpubdb01:1433;DatabaseName=pamreporting2042
sqlserver.datasource1.url=jdbc:sqlserver://fr1xpubdb01:1433;DatabaseName=PAMReporting301104
sqlserver.datasource1.username=pamreporting
sqlserver.datasource1.password=password
sqlserver.datasource1.driverClassName=com.microsoft.sqlserver.jdbc.SQLServerDriver

sqlserver.datasource2.url=jdbc:sqlserver://fr1xpubdb01:1433;DatabaseName=PAMReporting3101
sqlserver.datasource2.username=pamreporting
sqlserver.datasource2.password=password
sqlserver.datasource2.driverClassName=com.microsoft.sqlserver.jdbc.SQLServerDriver

java.security.auth.login.config=C:/ProgramDev/jdk1.7.0_51_64bit/jre/lib/security/jaas.conf
java.security.krb5.conf=C:/ProgramDev/jdk1.7.0_51_64bit/jre/lib/security/krb5.conf
```

```java
package com.ssgx.pamreport.test.dbcompare.service;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.ssgx.pamreport.test.dbcompare.config.ConfigFile;
import com.ssgx.pamreport.test.dbcompare.dao.ImpalaDAO;
import com.ssgx.pamreport.test.dbcompare.dao.SqlServerDAO;
import com.ssgx.pamreport.test.dbcompare.model.Column;
import com.ssgx.pamreport.test.dbcompare.model.Element;
import com.ssgx.pamreport.test.dbcompare.model.Mart;
import com.ssgx.pamreport.test.dbcompare.model.TestResult;
import com.ssgx.pamreport.test.dbcompare.model.TestResultMart;
import com.ssgx.pamreport.test.dbcompare.utils.TestUtils;

/**
 * ElementsCompareService
 *
 */
public class ElementsCompareService {

    private static TestResult testResult = new TestResult();

    private SqlServerDAO sqlServerDAO = new SqlServerDAO();
    private ImpalaDAO impalaDAO = new ImpalaDAO();

    private Boolean showRepeated = false;
    private List<Element> ignoredElements;

    public void init() {

    }

    public void compareMartAllElements(String martName) {
        openConnections();

        Mart mart = sqlServerDAO.getMartByName(martName);
        mart.setMappedTableName(martName);
        List<Element> elementsAll = mart.getElements();
        List<Column> colunsAll = impalaDAO.getColumnsByTableName(martName);
        compareMartImpalaList(mart, elementsAll, colunsAll);

        closeConnections();
    }

    public void compareAllMartAllElements() {
        openConnections();
        List<Mart> martList = sqlServerDAO.getAllMarts();
        for (Mart mart : martList) {
            System.out.println("@" + mart.getName());
            mart.setMappedTableName(mart.getName());
            List<Element> elementsAll = mart.getElements();
            List<Column> columnsAll = impalaDAO.getColumnsByTableName(mart.getName());
            compareMartImpalaList(mart, elementsAll, columnsAll);
        }
        closeConnections();
    }

    public void compareAllMartAllElementsNameOnly() {
        openConnections();
        List<Mart> martList = sqlServerDAO.getAllMarts();
        for (Mart mart : martList) {
            System.out.println("@" + mart.getName());
            mart.setMappedTableName(mart.getName());
            List<Element> elementsAll = mart.getElements();
            List<Column> columnsAll = impalaDAO.getColumnsByTableName(mart.getName());
            compareMartImpalaListNameOnly(mart, elementsAll, columnsAll);
        }
        closeConnections();
    }

    public void compareAllMartAllElementsNameOnly(String martName) {
        openConnections();
        Mart mart = sqlServerDAO.getMartByName(martName);
        System.out.println("@" + mart.getName());
        mart.setMappedTableName(mart.getName());
        List<Element> elementsAll = mart.getElements();
        List<Column> columnsAll = impalaDAO.getColumnsByTableName(mart.getName());
        compareMartImpalaListNameOnly(mart, elementsAll, columnsAll);
        closeConnections();
    }

    public void compareMartCoreElements(String martName) {
        openConnections();

        Mart mart = sqlServerDAO.getMartByName(martName);
        mart.setMappedTableName(mart.getName() + "_CORE");
        List<Element> elementsCore = mart.getElementsCore();

        List<Column> columnsCore = impalaDAO.getCoreColumnsByMartName(martName);
        compareMartImpalaList(mart, elementsCore, columnsCore);

        closeConnections();
    }

    public void compareMartTableElements(String martName, String tableName) {
        openConnections();

        Mart mart = sqlServerDAO.getMartByName(martName);
        System.out.println(mart);
        mart.setMappedTableName(tableName);

        List<Element> elements = mart.getElements();

        List<Column> columns = impalaDAO.getColumnsByTableName(tableName);
        compareMartImpalaList(mart, elements, columns);

        closeConnections();
    }

    public void compareMartTableCoreElements(String martName, String tableName) {
        openConnections();

        Mart mart = sqlServerDAO.getMartByName(martName);
        mart.setMappedTableName(tableName.toUpperCase());
        List<Element> elements = mart.getElementsCore();

        List<Column> columns = impalaDAO.getColumnsByTableName(tableName);
        compareMartImpalaList(mart, elements, columns);

        closeConnections();
    }

    public void compareAllMartCoreElements() {
        openConnections();

        List<Mart> martList = sqlServerDAO.getAllMarts();
        for (Mart mart : martList) {
            System.out.println("@" + mart.getName());
            mart.setMappedTableName(mart.getName() + "_CORE");
            List<Element> elementsCore = mart.getElementsCore();
            List<Column> columnsCore = impalaDAO.getColumnsByTableName(mart.getName() + "_CORE");
            compareMartImpalaList(mart, elementsCore, columnsCore);
        }
        closeConnections();
    }

    public void compareAllMartCoreElementsNameOnly() {
        openConnections();

        List<Mart> martList = sqlServerDAO.getAllMarts();
        for (Mart mart : martList) {
            System.out.println("@" + mart.getName());
            mart.setMappedTableName(mart.getName() + "_CORE");
            List<Element> elementsCore = mart.getElementsCore();
            List<Column> columnsCore = impalaDAO.getColumnsByTableName(mart.getName() + "_CORE");
            compareMartImpalaListNameOnly(mart, elementsCore, columnsCore);
        }
        closeConnections();
    }

    private void openConnections() {
        sqlServerDAO.getConnection();
        impalaDAO.getConnection();
    }

    private void closeConnections() {
        sqlServerDAO.closeConnection();
        impalaDAO.closeConnection();
    }

    private Boolean haveAllMatchedColumn(Column column, List<Element> elements) {
        Boolean haveMatched = false;
        for (Element element : elements) {
            Boolean nameMatched = strEquals(element.getName(), column.getName());
            Boolean typeMatched = strEquals(element.getType(), column.getType());
            if (nameMatched && typeMatched) {
                haveMatched = true;
                break;
            }
        }
        return haveMatched;
    }

    public void getIgnoredElements() {
        ignoredElements = ConfigFile.getIgnoredElements();
    }

    public void compareMartImpalaList(Mart mart, List<Element> elementList, List<Column> columns) {
        List<Element> elemntsNotMatched = new ArrayList<Element>();
        Map<Element, Column> typeNotMatchedMap = new HashMap<Element, Column>();

        TestResultMart testResultMart = new TestResultMart();
        testResultMart.setMartName(mart.getName());
        testResultMart.setTableName(mart.getMappedTableName());
        System.out.println("Mart:" + testResultMart.getMartName() + ":" + elementList.size());
        System.out.println("Impala:" + testResultMart.getTableName() + ":" + columns.size());
        Map<String, Boolean> haveMatchedMap = haveMatchedColumnMap(elementList, columns);
        for (Element element : elementList) {
            Boolean matched = false;
            Boolean repeated = (countElementNameRepeatTimes(element, elementList) > 1)
                    && (haveMatchedMap.get(element.getName()) != null);
            
            for (Column column : columns) {
                Boolean nameMatched = elementColumnNameMatched(element, column);
                Boolean typeMatched = elementColumnTypeMatched(element, column);
                
                if (nameMatched) {
                    matched = true;
                    Boolean haveAllMatched = haveAllMatchedColumn(column, elementList);
                    if(typeMatched){
                        columns.remove(column);
                    }else if(!haveAllMatched){
                        typeNotMatchedMap.put(element, column);
                        columns.remove(column);
                    }else{
                        matched = false;
                    }
                    break;
                }
            }
            if (!matched) {
                if (repeated) {
                    element.setName(element.getName() + "(Repeated)");
                    if (showRepeated) {
                        elemntsNotMatched.add(element);
                    }
                } else {
                    elemntsNotMatched.add(element);
                }
            }
        }

        getIgnoredElements();
        List<Element> elemntsNotMatchedFinal = new ArrayList<Element>();
        for (Element notMatchedET : elemntsNotMatched) {
            boolean isIgnored = false;
            for (Element ignoredElement : ignoredElements) {
                if (strEquals(notMatchedET.getName(), ignoredElement.getName())
                        && strEquals(notMatchedET.getType(), ignoredElement.getType())) {
                    isIgnored = true;
                    break;
                }
            }

            if (!isIgnored) {
                elemntsNotMatchedFinal.add(notMatchedET);
            }
        }

        testResultMart.setNotMatchedElement(elemntsNotMatchedFinal);
        testResultMart.setNotMatchedColumns(columns);
        testResultMart.setNotMatchedTypeMap(typeNotMatchedMap);
        testResult.getTestResultMartList().add(testResultMart);
    }

    public void compareMartImpalaListNameOnly(Mart mart, List<Element> elementList, List<Column> columns) {
        List<Element> elemntsNotMatched = new ArrayList<Element>();
        Map<Element, Column> typeNotMatchedMap = new HashMap<Element, Column>();

        TestResultMart testResultMart = new TestResultMart();
        testResultMart.setMartName(mart.getName());
        testResultMart.setTableName(mart.getMappedTableName());
        System.out.println("Mart:" + testResultMart.getMartName() + ":" + elementList.size());
        System.out.println("Impala:" + testResultMart.getTableName() + ":" + columns.size());

        Map<String, Boolean> haveMatchedMap = haveMatchedColumnNameOnlyMap(elementList, columns);
        for (Element element : elementList) {
            Boolean matched = false;
            Boolean repeated = (countElementNameRepeatTimes(element, elementList) > 1)
                    && (haveMatchedMap.get(element.getName()) != null);
            
            for (Column column : columns) {
                Boolean nameMatched = elementColumnNameMatched(element, column);
                if (nameMatched) {
                    matched = true;
                    if (repeated && !elementColumnTypeMatched(element, column)) {
                        matched = false;
                    } else {
                        columns.remove(column);
                    }
                    break;
                }
            }
            
            if (!matched) {
                if (repeated) {
                    element.setName(element.getName() + "(Repeated)");
                    if (showRepeated) {
                        elemntsNotMatched.add(element);
                    }
                } else {
                    elemntsNotMatched.add(element);
                }
            }
        }

        getIgnoredElements();
        List<Element> elemntsNotMatchedFinal = new ArrayList<Element>();
        for (Element notMatchedET : elemntsNotMatched) {

            boolean isIgnored = false;
            for (Element ignoredElement : ignoredElements) {
                if (strEquals(notMatchedET.getName(), ignoredElement.getName())
                        && strEquals(notMatchedET.getType(), ignoredElement.getType())) {
                    isIgnored = true;
                    break;
                }
            }

            if (!isIgnored) {
                elemntsNotMatchedFinal.add(notMatchedET);
            }
        }

        testResultMart.setNotMatchedElement(elemntsNotMatchedFinal);
        testResultMart.setNotMatchedColumns(columns);
        testResultMart.setNotMatchedTypeMap(typeNotMatchedMap);
        testResult.getTestResultMartList().add(testResultMart);
    }

    private Map<String, Boolean> haveMatchedColumnNameOnlyMap(List<Element> elementList, List<Column> columnList) {
        HashMap<String, Boolean> result = new HashMap<String, Boolean>();

        for (Element element : elementList) {
            for (Column column : columnList) {
                if (strEquals(element.getName(), column.getName())) {
                    result.put(element.getName(), true);
                    break;
                }
            }
        }
        return result;
    }
    
    private Map<String, Boolean> haveMatchedColumnMap(List<Element> elementList, List<Column> columnList) {
        HashMap<String, Boolean> result = new HashMap<String, Boolean>();

        for (Element element : elementList) {
            for (Column column : columnList) {
                if (elementColumnNameTypeMatched(element, column)) {
                    result.put(element.getName(), true);
                    break;
                }
            }
        }
        return result;
    }

    private Integer countElementNameRepeatTimes(Element element, List<Element> elements) {
        int result = 0;
        for (Element et : elements) {
            if (strEquals(element.getName(), et.getName())) {
                result++;
            }
        }
        return result;
    }
    
    private Boolean elementColumnNameTypeMatched(Element element, Column column) {
        return elementColumnNameMatched(element, column ) && elementColumnTypeMatched(element, column );
    }
    
    private Boolean elementColumnNameMatched(Element element, Column column) {
        return strEquals(element.getName(), column.getName());
    }

    private Boolean elementColumnTypeMatched(Element element, Column column) {
        return strEquals(element.getType(), column.getType());
    }

    public void writeResultToFiles() throws IOException {
        writeResultToFiles("");
    }

    public void writeResultToFiles(String suffix) throws IOException {
        TestUtils.writeResultToFiles(testResult, suffix);
    }

    private Boolean strEquals(String a, String b) {
        return a.toUpperCase().equals(b.toUpperCase());
    }

    public TestResult getCompareResult() {
        return testResult;
    }

    public void setCompareResult(TestResult compareResult) {
        ElementsCompareService.testResult = compareResult;
    }

    public Boolean getShowRepeated() {
        return showRepeated;
    }

    public void setShowRepeated(Boolean showRepeated) {
        this.showRepeated = showRepeated;
    }

}
```
###输出报表样例
最后将结果填充到HTML文件中，并根据Mart名字来生成 
![TestResult](TestReport.gif)
