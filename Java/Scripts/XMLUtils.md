### XML Utils
> 2:46 PM 2/22/2018 currently, there is only the method to read object from xml ty XPath
```Java
package com.ssgx.pamreport.test.dbcompare.utils;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;

import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.JDOMException;
import org.jdom2.filter.Filters;
import org.jdom2.input.SAXBuilder;
import org.jdom2.xpath.XPathExpression;
import org.jdom2.xpath.XPathFactory;

public class XMLUtils {
    public static void main(String[] args) {
        try {
            readXML();
        } catch (JDOMException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    public static String getValueByExpression(String filePath, String expression) throws JDOMException, IOException{
        String result = "";
        //filePath = "file:." + filePath;
        InputStream in = XMLUtils.class.getClassLoader().getResourceAsStream(filePath);
        //InputStream in = new PathMatchingResourcePatternResolver().getResource(filePath).getInputStream();
        SAXBuilder builder = new SAXBuilder();
        Document document = builder.build(in);

        // create xpath factory
        XPathFactory xpath = XPathFactory.instance();

        XPathExpression<Element> expr = xpath.compile(expression, Filters.element());
        List<Element> queries = expr.evaluate(document);
        for (Element query : queries){
            result =  query.getValue().trim();
        }
        
        return result;
    }
    
    public static void readXML() throws JDOMException, IOException{
        InputStream in = XMLUtils.class.getResourceAsStream("/query_sqlserver.xml");
        SAXBuilder builder = new SAXBuilder();
        Document document = builder.build(in);

        // create xpath factory
        XPathFactory xpath = XPathFactory.instance();

        XPathExpression<Element> expr = xpath.compile("//queries/query[@id='1']", Filters.element());
        List<Element> query = expr.evaluate(document);
        for (Element course : query){
            System.out.println("   " + course.getValue().trim());
        }

/*        System.out.println("\n2. select all attributes of element");
        XPathExpression<Attribute> attrExpr = xpath.compile("//course/@id", Filters.attribute());
        List<Attribute> ids = attrExpr.evaluate(document);
        for (Attribute id : ids){
            System.out.println("   " + id.getValue());
        }

        System.out.println("\n3. select the second element");
        expr = xpath.compile("//course[2]/name", Filters.element());
        Element name = expr.evaluateFirst(document);
        System.out.println("   " + name.getValue());

        System.out.println("\n4. select element by xpath with attribute");
        expr = xpath.compile("//course[@id='1']/name", Filters.element());
        Element child = expr.evaluateFirst(document);
        System.out.println("   " + child.getValue());*/
    }
}
```
