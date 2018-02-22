package com.ssgx.pamreport.test.dbcompare.utils;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.Map;

import org.apache.commons.codec.Charsets;
import org.apache.commons.io.FileUtils;

import com.ssgx.pamreport.test.dbcompare.model.Column;
import com.ssgx.pamreport.test.dbcompare.model.Element;
import com.ssgx.pamreport.test.dbcompare.model.TestResult;
import com.ssgx.pamreport.test.dbcompare.model.TestResultMart;

public class TestUtils {

    public static void writeResultToFiles(TestResult testResult, String suffix) throws IOException {
        
        URL url = TestUtils.class.getClassLoader().getResource("Template.html");
                //.getResourceAsStream("Template.html").
        //URL url = new PathMatchingResourcePatternResolver().getResource("file:./Template.html").getURL();
        File htmlTemplateFile = new File(url.getPath());
        // File htmlTemplateFile = new File("./Template.html");

        String tableStr = "";
        String htmlTemplate = FileUtils.readFileToString(htmlTemplateFile, Charsets.toCharset("UTF-8"));
        String contentTemplate = "<tr><td>%s</td><td>%s</td><td class='elementType'>%s</td><td>%s</td><td>%s</td><td class='columnType'>%s</td></tr>";

        for (TestResultMart trm : testResult.getTestResultMartList()) {
            int notMatchedEltNum = trm.getNotMatchedElement().size();
            int notMatchedColNum = trm.getNotMatchedColumns().size();

            Map<Element, Column> map = trm.getNotMatchedTypeMap();

            boolean flag1 = notMatchedEltNum > 0;
            boolean flag2 = !map.isEmpty();
            boolean flag3 = notMatchedColNum > 0 && trm.getTableName().contains("CORE");
            if (flag1 || flag2 || flag3) {
                for (Element element : trm.getNotMatchedElement()) {
                    tableStr += String.format(contentTemplate, trm.getMartName(), element.getName(), element.getType(),
                            trm.getTableName(), "", "");
                }
                if (trm.getTableName().contains("CORE")) {
                    for (Column column : trm.getNotMatchedColumns()) {
                        tableStr += String.format(contentTemplate, trm.getMartName(), "", "", trm.getTableName(),
                                column.getName(), column.getType());
                    }
                }

                for (Element key : map.keySet()) {
                    tableStr += String.format(contentTemplate, trm.getMartName(), key.getName(), key.getType(),
                            trm.getTableName(),
                            map.get(key).getIsCore() ? map.get(key).getName() + "(CORE)" : map.get(key).getName(),
                            map.get(key).getType());
                }

                String htmlOut = replaceContent(htmlTemplate, "resultItem", tableStr);
               
                String fileName = trm.getMartName() + suffix + ".html";

                FileUtils.writeStringToFile(new File("TestResult/" + fileName), htmlOut,
                        Charsets.toCharset("UTF-8"));

                tableStr = "";
            }
        }

        testResult.getTestResultMartList().clear();

        // Desktop.getDesktop().browse(URI.create("Result.html"));

    }
    public static String replaceContent(String original, String key, String value) {
        return original.replaceAll("\\{" + key + "\\}", value);
    }

}
