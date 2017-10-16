package org.bearfly.tools;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

import org.apache.log4j.LogManager;
import org.apache.log4j.Logger;

public class FileUtils {
    private final static Logger log = LogManager.getLogger(FileUtils.class);
    public static void findText(String textSearched, String filePath, Boolean caseSensitive) throws IOException{
        File root   = new File(filePath);
        if (root.isDirectory()) {
            File[] leaves = root.listFiles();
            for(int i = 0; i < leaves.length;i++){
                findText(textSearched, leaves[i].getAbsolutePath(), caseSensitive);
            }
        }else{
            BufferedReader br   = new BufferedReader(new FileReader(root));
            StringBuffer sb     = new StringBuffer("");
            String lineText     = br.readLine();
            while(!(lineText == null)){
                sb.append(lineText);
                lineText        = br.readLine();
            }
            if (caseSensitive){
                if (sb.toString().contains(textSearched)){
                    log.info(root.getAbsolutePath());
                }
            }else{ 
                if (sb.toString().toLowerCase().contains(textSearched.toLowerCase())){
                    log.info(root.getAbsolutePath());
                }
            }
            br.close();
        }
        
    }
    public static void findText(String textSearched, String filePath) throws IOException{
        findText(textSearched, filePath, false);
    }
    public static void main(String[] args) {
        try {
            FileUtils.findText("org.bearfly.tools", "C:/Users/chenx/Desktop/GitSpace", false);
//            FileUtils.findText("PowerShell", "C:/Users/chenx/Desktop/aa");
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
}
