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
