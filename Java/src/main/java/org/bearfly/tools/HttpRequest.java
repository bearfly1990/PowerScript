package org.bearfly.tools;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.URL;
import java.net.URLConnection;
import java.util.List;
import java.util.Map;

import org.apache.log4j.LogManager;
import org.apache.log4j.Logger;


public class HttpRequest {
    public static final Logger log = LogManager.getLogger(HttpRequest.class);
    public static String sendGet(String urlstr, Map<String, String>...params) {
        String result = "";
        BufferedReader in = null;
        urlstr = urlstr + "?";
        try {
            for (Map<String, String> param : params) {
                for(String key : param.keySet()){
                    urlstr = urlstr + key +"="+ param.get("key");
                }
                
            }
            log.debug(urlstr);
            URL url = new URL(urlstr);
           
            URLConnection conn = url.openConnection();
            conn.setRequestProperty("accept", "*/*");
            conn.setRequestProperty("connection", "Keep-Alive");
            conn.setRequestProperty("user-agent","JavaSE1.8/Eclipse");
            conn.connect();
            Map<String, List<String>> map = conn.getHeaderFields();
            for (String key : map.keySet()) {
                log.info(formatOutput(key, 30) + map.get(key));
            }
            in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
            String line;
            while ((line = in.readLine()) != null) {
                result += line;
            }
            in.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return result;
    }
    public static String sendPost(String urlstr, String param) {
        PrintWriter out = null;
        BufferedReader in = null;
        String result = "";
        try {
            URL realUrl = new URL(urlstr);
            URLConnection conn = realUrl.openConnection();
            conn.setRequestProperty("accept", "*/*");
            conn.setRequestProperty("connection", "Keep-Alive");
            conn.setRequestProperty("user-agent","JavaSE1.8/Eclipse");
            conn.setDoOutput(true);
            conn.setDoInput(true);
            out = new PrintWriter(conn.getOutputStream());
            out.print(param);
            out.flush();
            in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
            String line;
            while ((line = in.readLine()) != null) {
                result += line;
            }
            out.close();
            in.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
      
        return result;
    }    
    public static String formatOutput(String str, int len){
        if (str != null && str.length() < len){
            str = str + appendString("-", len - str.length());
        }
        return str +"->";
    }
    public static String appendString(String str, int factor){
        StringBuffer result = new StringBuffer("");
        for(int i = 0; i < factor; i++){
            result.append(str);
        }
        return result.toString();
    }
}
