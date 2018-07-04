### Deploy UVT Enviroment
每次有新的Build生成，方便的把测试环境给部署好。
```python
import glob
import os
import shutil
import subprocess
import zipfile
import logging
g_UVTWorkSpace = r"xxx\UVT_WorkSpace"
g_ConfigFilePath = g_UVTWorkSpace + r"\ConfigFile\xxx.xml"
g_UVTDir = g_UVTWorkSpace + r"\xxx\\"
g_UVTEXE = g_UVTDir + "\xxx.exe"
g_ZipFileName = "xxx"
g_ZipFileFullName = g_ZipFileName + ".zip"
g_ZipExtactDir = g_ZipFileName
g_BuildedZipFilePath = r"\\xxx\Builds\\"+ g_ZipFileFullName
def __main__():
    logging.basicConfig(filename='_DeployUVT.log', level=logging.INFO, format='%(asctime)s %(message)s')
    try:
        # print(os.path.isdir(g_UVTDir))
        if (os.path.exists(g_UVTDir)):
            shutil.rmtree(g_UVTDir)
            logging.info("Remove old Directory {0} succussfully".format(g_UVTDir))
        if(os.path.exists(g_ZipFileFullName)):
            os.remove(g_ZipFileFullName)
            logging.info("Remove old build zip {0} succussfully".format(g_ZipFileFullName))
        shutil.copy(g_BuildedZipFilePath, g_UVTWorkSpace)
        logging.info("Copy new build zip {0} succussfully".format(g_BuildedZipFilePath))
        zip_ref = zipfile.ZipFile(g_ZipFileFullName, 'r')
        zip_ref.extractall(g_ZipExtactDir)
        zip_ref.close()
        logging.info("Unzip new build zip to {0} succussfully".format(g_ZipExtactDir))
        shutil.copy(g_ConfigFilePath, g_UVTDir)
        logging.info('Copy config xml file:{0} succussfully'.format(g_ConfigFilePath))
        logging.info("run UVT exe...")
        subprocess.Popen([g_UVTEXE])
    except IOError as e:
        # print("Unable handle file. %s" % e)
        logging.error(e)
    except:
        # print("Unexpected error:", sys.exc_info())
        logging.error(e)


__main__()
```
  
  
