package org.bearfly.tools;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

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
    
    public static void EncodeFile(String src, String target) throws IOException{
        final int key = 0x18;
        EncodeFile(src, target, key);
    }
    
    public static void EncodeFile(String src, String target, final int key) throws IOException{
        File srcFile = new File(src);
        File tgtFile = new File(target);
        if(!srcFile.exists()){
            log.error("Source File Not Exist");
        }else{
            if(!tgtFile.exists()){
                log.info("Target File Not Exist, Is Created Now");
                tgtFile.createNewFile();
            }
            InputStream fis = new FileInputStream(srcFile);
            OutputStream fos = new FileOutputStream(target);
            int dataOfFile;
            while ((dataOfFile = fis.read()) > -1) {
                fos.write(dataOfFile^key);
            }
            fis.close();
            fos.flush();
            fos.close();
        }
    }
    public static void DecodeFile(String src, String target, final int key) throws IOException{
        File srcFile = new File(src);
        File tgtFile = new File(target);
        if(!srcFile.exists()){
            log.error("Encoded File Not Exist");
        }else{
            if(!tgtFile.exists()){
                log.info("Target Decoded File Not Exist, Is Created Now");
                tgtFile.createNewFile();
            }
            InputStream fis = new FileInputStream(srcFile);
            OutputStream fos = new FileOutputStream(target);
            int dataOfFile;
            while ((dataOfFile = fis.read()) > -1) {
                fos.write(dataOfFile^key);
            }
            fis.close();
            fos.flush();
            fos.close();
        }
    }
    public static void DecodeFile(String src, String target) throws IOException{
        final int key = 0x18;
        DecodeFile(src, target, key);
    }
    public static void main(String[] args) {
        try {
            //FileUtils.findText("org.bearfly.tools", "C:/Users/chenx/Desktop/GitSpace", false);
//            FileUtils.findText("PowerShell", "C:/Users/chenx/Desktop/aa");
            FileUtils.EncodeFile("C:/Users/chenx/Desktop/1.txt", "C:/Users/chenx/Desktop/2.txt");
            FileUtils.DecodeFile("C:/Users/chenx/Desktop/2.txt", "C:/Users/chenx/Desktop/3.txt");
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
}
