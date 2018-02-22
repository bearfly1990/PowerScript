package com.ssgx.pamreport.test.dbcompare.utils;

import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

import org.jdom2.JDOMException;

import com.ssgx.pamreport.test.dbcompare.config.ConfigFile;

public class JDBCUtils {
    public static Connection getConnection(String driver, String url, String user, String pwd)
            throws SQLException, ClassNotFoundException {

        System.getProperties().setProperty("javax.security.auth.useSubjectCredsOnly", "false");
        System.getProperties().setProperty("java.security.auth.login.config",
               ConfigFile.getProperty("java.security.auth.login.config"));
        System.getProperties().setProperty("java.security.krb5.conf",
                ConfigFile.getProperty("java.security.krb5.conf"));

        Class.forName(driver);
        return DriverManager.getConnection(url, user, pwd);
    }

    public static Connection getConnectionByProperties(String driverKeyStr, String urlKeyStr, String userKeyStr,
            String pwdKeyStr) throws ClassNotFoundException, SQLException {
        
        Connection connection = null;
        String driver = ConfigFile.getProperty(driverKeyStr);
        String url = ConfigFile.getProperty(urlKeyStr);
        String user = ConfigFile.getProperty(userKeyStr);
        String password = ConfigFile.getProperty(pwdKeyStr);
        //logger.info("url=" + url + ", driver=" + driver + ", user=" + user);
        if (url == null || driver == null || user == null) {
            System.out.println("Unable to get db connection infor : " + ConfigFile.getPropertyFilePath());
            //logger.error("Unable to get db connection infor : " + ConfigFile.getPropertyFilePath());
           // logger.error("url=" + url + ", driver=" + driver + ", user=" + user);
        } else {
            connection =  JDBCUtils.getConnection(driver, url, user, password);
        }
        
        return connection;
    }
    
    public static String getQueryStr(String filePath, String queryStr) {
        String result = "";
        try {
            result = XMLUtils.getValueByExpression(filePath, queryStr);
        } catch (JDOMException | IOException e) {
            e.printStackTrace();
        }
        return result;
    }
}
