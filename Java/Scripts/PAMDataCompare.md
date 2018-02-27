# PAM Data Compare

PAM Data in BA Server is stored in the SqlServer DB, it has his own logic to store the data.
The Original PAM Data is Stored in Impala.

BA Server 将mart的信息分布在不同的几张表中，首先需要用sql把表连接起来得到数据。
sample as below：
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

而PAM这边就比较简单：
```sql
--query_impala.xml
    describe  %s
```

```html
<!DOCTYPE html>
<html>
<head>
<title>Test Result</title>
<link rel="Stylesheet" type="text/css"
	href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
</link>
<style>
table {
	border-collapse: collapse;
	width: 100%;
}

th, td {
	padding: 8px;
	text-align: left;
	border-bottom: 1px solid #ddd;
}

td.elementType {
	color: #00F;
}

td.columnType {
	color: #F01B2D
}

tr:hover {
	background-color: #f5f5f5;
}
</style>
</head>
<body class="container">
	<h1>Test Result</h1>
	<!-- <span>${ResultTxt}</span> -->
	<div id="testResult">
		<!-- Table markup-->
		<table id="...">
			<thead>
				<tr>
					<th scope="col" id="">Mart Name</th>
					<th scope="col" id="">Mart Element</th>
					<th scope="col" id="">Mart Element Type</th>
					<th scope="col" id="">Impala Table </th>
					<th scope="col" id="">Impala Column</th>
					<th scope="col" id="">Impala Column Type</th>
				</tr>
			</thead>
			<tfoot>
				<!-- <tr>
					<td>End...</td>
					<td>End...</td>
					<td>End...</td>
					<td>End...</td>
					<td>End...</td>
					<td>End...</td>
				</tr> -->
			</tfoot>
			<!-- Table body -->
			<tbody>
				{resultItem}
				<!--  <tr>
                        <td>MartNameF</td>
                        <td>ASOF</td>
                        <td>int</td>
                         <td>TableName</td>
                        <td>ASOF</td>
                        <td>String</td>
                    </tr> -->
			</tbody>

		</table>
	</div>
</body>
</html>

```

```
#compare mode :
#1 : compare two database's table data
#2:  compare two database's table key columns (and need to set another database for comparison )  note: 3 database must in same impala
compareMode=1

# Replace with your connection string
#impala.datasource1.url=jdbc:impala://hadoop01.xcts.pr1:21050/psdb1300v20502
impala.datasource1.url=jdbc:impala://hadoop07.dev.pr1.eexchange.com:21050/metldw595d;SSL=1;CAIssuedCertNamesMismatch=1;SSLTrustStore=C:/ProgramDev/jdk1.7.0_51_64bit/jre/lib/security/cacerts;SSLTrustStorePwd=changeit;AuthMech=1;KrbServiceName=impala;KrbAuthType=1;KrbRealm=CURNX.COM;KrbHostFQDN=hadoop07.dev.pr1.eexchange.com;

# Replace with your credentials
impala.datasource1.username=
impala.datasource1.password=
impala.datasource1.driverClassName=com.cloudera.impala.jdbc41.Driver


# Replace with your connection string
#sqlserver.datasource1.url=jdbc:sqlserver://fr1xpubdb01:1433;DatabaseName=pamreporting2042
sqlserver.datasource1.url=jdbc:sqlserver://fr1xpubdb01:1433;DatabaseName=PAMReporting301104
# Replace with your credentials
sqlserver.datasource1.username=pamreporting
sqlserver.datasource1.password=password
sqlserver.datasource1.driverClassName=com.microsoft.sqlserver.jdbc.SQLServerDriver

# Replace with your connection string
#sqlserver.datasource1.url=jdbc:sqlserver://fr1xpubdb01:1433;DatabaseName=pamreporting2042
sqlserver.datasource2.url=jdbc:sqlserver://fr1xpubdb01:1433;DatabaseName=PAMReporting3101
# Replace with your credentials
sqlserver.datasource2.username=pamreporting
sqlserver.datasource2.password=password
sqlserver.datasource2.driverClassName=com.microsoft.sqlserver.jdbc.SQLServerDriver


java.security.auth.login.config=C:/ProgramDev/jdk1.7.0_51_64bit/jre/lib/security/jaas.conf
java.security.krb5.conf=C:/ProgramDev/jdk1.7.0_51_64bit/jre/lib/security/krb5.conf





```
```maven
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>

	<groupId>com.ssgx.amreport.test</groupId>
	<artifactId>PAMReportTest</artifactId>
	<version>0.0.1-SNAPSHOT</version>
	<packaging>jar</packaging>

	<name>PAMReportTest</name>
	<url>http://maven.apache.org</url>

	<properties>
		<project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
		<org.slf4j-version>1.7.5</org.slf4j-version>
		<org.springframework-version>4.2.7.RELEASE</org.springframework-version>
	</properties>

	<build>
		<finalName>PAMReportTest</finalName>
		<plugins>
			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-compiler-plugin</artifactId>
				<version>3.1</version>
				<configuration>
					<source>1.7</source>
					<target>1.7</target>
				</configuration>
			</plugin>

			<!-- Maven Assembly Plugin -->
			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-assembly-plugin</artifactId>
				<version>2.4.1</version>
				<configuration>
					<!-- get all project dependencies -->
					<descriptorRefs>
						<descriptorRef>jar-with-dependencies</descriptorRef>
					</descriptorRefs>
					<!-- MainClass in manifest make a executable jar -->
					<archive>
						<manifest>
							<mainClass>com.ssgx.pamreport.test.dbcompare.ElementCompareMain</mainClass>
						</manifest>
					</archive>

				</configuration>
				<executions>
					<execution>
						<id>make-assembly</id>
						<!-- bind to the packaging phase -->
						<phase>package</phase>
						<goals>
							<goal>single</goal>
						</goals>
					</execution>
				</executions>
			</plugin>

			<plugin>
				<artifactId>maven-resources-plugin</artifactId>
				<version>2.6</version>
				<executions>
					<execution>
						<id>copy-resources</id>
						<phase>validate</phase>
						<goals>
							<goal>copy-resources</goal>
						</goals>
						<configuration>
							<outputDirectory>${project.build.directory}</outputDirectory>
							<resources>
								<resource>
									<directory>./</directory>
									<includes>
										<include>DBInfo.properties</include>
										<include>query_impala.xml</include>
										<include>query_sqlserver.xml</include>
										<include>Template.html</include>
										<include>ignoredElements.txt</include>
									</includes>
								</resource>
							</resources>
						</configuration>
					</execution>
				</executions>
			</plugin>
		</plugins>
	</build>

	<dependencies>
		<dependency>
			<groupId>com.opencsv</groupId>
			<artifactId>opencsv</artifactId>
			<version>3.9</version>
		</dependency>
		<!-- Spring -->
		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-context</artifactId>
			<version>${org.springframework-version}</version>
			<exclusions>
				<exclusion>
					<groupId>commons-logging</groupId>
					<artifactId>commons-logging</artifactId>
				</exclusion>
			</exclusions>

		</dependency>

		<dependency>
			<groupId>com.cloudera.impala.jdbc</groupId>
			<artifactId>ImpalaJDBC41</artifactId>
			<version>2.5.30</version>
		</dependency>

		<dependency>
			<groupId>org.apache.thrift</groupId>
			<artifactId>libthrift</artifactId>
			<version>0.9.0</version>
		</dependency>
		<dependency>
			<groupId>com.microsoft.sqlserver</groupId>
			<artifactId>mssql-jdbc</artifactId>
			<version>6.1.0.jre7</version>
		</dependency>
		<dependency>
			<groupId>com.cloudera.impala</groupId>
			<artifactId>ql</artifactId>
			<version>1.0</version>
		</dependency>
		<dependency>
			<groupId>com.cloudera.impala</groupId>
			<artifactId>hive-service</artifactId>
			<version>1.0</version>
		</dependency>
		<dependency>
			<groupId>org.apache.thrift</groupId>
			<artifactId>libfb303</artifactId>
			<version>0.9.0</version>
		</dependency>
		<dependency>
			<groupId>com.cloudera.impala</groupId>
			<artifactId>hive-metastore</artifactId>
			<version>1.0</version>
		</dependency>
		<dependency>
			<groupId>com.cloudera.impala</groupId>
			<artifactId>tici-service-client</artifactId>
			<version>1.0</version>
		</dependency>
		<dependency>
			<groupId>org.apache.zookeeper</groupId>
			<artifactId>zookeeper</artifactId>
			<version>3.4.6</version>
		</dependency>
		<!-- Logging -->
		<dependency>
			<groupId>org.slf4j</groupId>
			<artifactId>slf4j-api</artifactId>
			<version>1.7.5</version>
		</dependency>
		<dependency>
			<groupId>org.slf4j</groupId>
			<artifactId>jcl-over-slf4j</artifactId>
			<version>1.7.5</version>
		</dependency>
		<dependency>
			<groupId>org.slf4j</groupId>
			<artifactId>slf4j-log4j12</artifactId>
			<version>1.7.5</version>
		</dependency>
		<dependency>
			<groupId>log4j</groupId>
			<artifactId>log4j</artifactId>
			<version>1.2.17</version>
			<!-- <exclusions> <exclusion> <groupId>javax.mail</groupId> <artifactId>mail</artifactId> 
				</exclusion> <exclusion> <groupId>javax.jms</groupId> <artifactId>jms</artifactId> 
				</exclusion> <exclusion> <groupId>com.sun.jdmk</groupId> <artifactId>jmxtools</artifactId> 
				</exclusion> <exclusion> <groupId>com.sun.jmx</groupId> <artifactId>jmxri</artifactId> 
				</exclusion> </exclusions> -->
		</dependency>
		<dependency>
			<groupId>junit</groupId>
			<artifactId>junit</artifactId>
			<version>4.2</version>
			<scope>test</scope>
		</dependency>
		<dependency>
			<groupId>org.jdom</groupId>
			<artifactId>jdom2</artifactId>
			<version>2.0.6</version>
		</dependency>
		<dependency>
			<groupId>jaxen</groupId>
			<artifactId>jaxen</artifactId>
			<version>1.1.6</version>
		</dependency>
		<dependency>
			<groupId>com.github.fmcarvalho</groupId>
			<artifactId>htmlflow</artifactId>
			<version>1.2</version>
		</dependency>
		<dependency>
			<groupId>commons-io</groupId>
			<artifactId>commons-io</artifactId>
			<version>2.5</version>
		</dependency>
	</dependencies>
</project>
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
