#个人桌面为中文
export LANG=en_US
xdg-user-dirs-gtk-update
export LANG=zh_CN.UTF-8
xdg-user-dirs-gtk-update

#耳机没声音
sudo apt install pavucontrol
pavucontrol

#更新 Adobe Flash player
sudo apt-get update
sudo apt-get install flashplugin-installer

#Ubuntu下的安装notepad++
sudo add-apt-repository ppa:notepadqq-team/notepadqq
sudo apt-get update
sudo apt-get install notepadqq
#Ubuntu下的卸载方法:
sudo apt-get remove notepadqq
sudo add-apt-repository --remove ppa:notepadqq-team/notepadqq

#安装Chrome
sudo wget http://www.linuxidc.com/files/repo/google-chrome.list -P /etc/apt/sources.list.d/
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -

#安装Mysql
sudo apt-get install mysql-server

sudo apt-get install mysql-client

sudo apt-get install libmysqlclient-dev

#安装过程中会提示设置密码什么的，注意设置了不要忘了，安装完成之后可以使用如下命令来检查是否安装成功：

sudo netstat -tap | grep mysql

#通过上述命令检查之后，如果看到有mysql 的socket处于 listen 状态则表示安装成功。

#登陆mysql数据库可以通过如下命令：

mysql -u root -p

#-u 表示选择登陆的用户名， -p 表示登陆的用户密码，上面命令输入之后会提示输入密码，此时输入密码就可以登录到mysql。

#解压
tar -zxvf apache-maven-3.3.9-bin.tar.gz  -C /usr/local

#删除目录
rm -rf /home/bearfly/temp

#复制
cp

#linux中在终端打开文件夹命令
gnome-open /etc
ubuntu中  nautilus /etc