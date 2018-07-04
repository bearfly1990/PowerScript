#个人桌面为中文
export LANG=en_US
xdg-user-dirs-gtk-update
export LANG=zh_CN.UTF-8
xdg-user-dirs-gtk-update

#耳机没声音
sudo apt install pavucontrol
pavucontrol

#更新 Adobe Flash player#####################################
sudo apt-get update
sudo apt-get install flashplugin-installer

#Ubuntu下的安装notepad++################################
sudo add-apt-repository ppa:notepadqq-team/notepadqq
sudo apt-get update
sudo apt-get install notepadqq
#Ubuntu下的卸载方法:##########################################
sudo apt-get remove notepadqq
sudo add-apt-repository --remove ppa:notepadqq-team/notepadqq

#安装Chrome###############################################
sudo wget http://www.linuxidc.com/files/repo/google-chrome.list -P /etc/apt/sources.list.d/
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -

#安装Mysql#################################################
sudo apt-get install mysql-server

sudo apt-get install mysql-client

sudo apt-get install libmysqlclient-dev

#安装过程中会提示设置密码什么的，注意设置了不要忘了，安装完成之后可以使用如下命令来检查是否安装成功：

sudo netstat -tap | grep mysql

#通过上述命令检查之后，如果看到有mysql 的socket处于 listen 状态则表示安装成功。

#登陆mysql数据库可以通过如下命令：

mysql -u root -p

#-u 表示选择登陆的用户名， -p 表示登陆的用户密码，上面命令输入之后会提示输入密码，此时输入密码就可以登录到mysql。

#解压############################################################
tar -zxvf apache-maven-3.3.9-bin.tar.gz  -C /usr/local

#删除目录##########################################################
rm -rf /home/bearfly/temp

#复制#####################################
cp

#linux中在终端打开文件夹命令#########################################
gnome-open /etc
ubuntu中  nautilus /etc

#linux下安装录制视频软件Simple Screen Recorder###############################################
sudo add-apt-repository ppa:maarten-baert/simplescreenrecorder
sudo apt-get update
sudo apt-get install simplescreenrecorder

#linux下安装Node.js######################################################
#下载node.js
http://nodejs.cn/download/
#解压并挪到目录下
tar -zxvf zxf node-v6.3.1-linux-x64.tar.gz   -C /usr/local/node
mv node-v6.3.1-linux-x64 /usr/local/node
cd /usr/bin
# 建立node软连
ln -s /usr/local/node/bin/node node
# 建立npm软连
ln -s /usr/local/node/bin/npm npm
#建立npx软连
ln -s /home/bearfly/DevPrograms/node-v8.9.3-linux-x64/bin/npx npx
ln -s /home/bearfly/DevPrograms/node-v8.查看方法：

#清空回收站##################################################
rm /home/bearfly/.local/share/Trash/expunged/* -r
rm /home/bearfly/.local/share/Trash/files/* -r
rm /home/bearfly/.local/share/Trash/info/* -r

#使用USB
sudo mount -t vfat /dev/sdb1 /mnt/usb
umount /dev/sdb1

