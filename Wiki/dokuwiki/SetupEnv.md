## Apache HTTP Server 2.4 配置支持PHP7，解决各种.dll缺失问题(转)

最近配置 Apache 2.4 支持PHP7，能够正常运行，扩展PHP7的extensions的时候，出现缺少libssh2.dll,libcrypto-1_1-x64.dll,LIBPQ.dll,icuuc60.dll的报错，尝试过各种解决方案，都不行，后来直接把PHP安装路径添加到path环境变量中就解决了。

下面记录一下：

服务器：Windows Server 2012 R2 Standard

Apache: httpd-2.4.29-o102n-x64-vc14-r2

PHP:php-7.2.3-Win32-VC15-x64

提前安装VC15 

### 一、Apache HTTP Server 2.4 的配置。

1.打开conf文件夹下面的httpd.conf文件

2.分别查找以下关键字，并修改，如下
```xml

Define SRVROOT "E:\mysever\Apache24"
ServerRoot "${SRVROOT}"

Listen 80

ServerName localhost:80


DocumentRoot "E:/mysever/Apache24/htdocs"

<Directory "E:/mysever/Apache24/htdocs">
```

### 二、PHP7的配置

#### 1.打开PHP7的安装文件目录，找到php.ini-production，复制一份，文件名修改为：php.ini，放回原目录。

#### 2.php.ini，查找以下关键字，并修改内容（把前面的“；”号去掉，代表启用这行代码），如下：
```ini
; extension_dir = "./"
; On windows:
extension_dir = "E:\mysever\php7\ext"


extension=bz2
extension=curl
extension=fileinfo
extension=gd2
extension=gettext
extension=gmp
extension=intl
extension=imap
;extension=interbase
;extension=ldap
extension=mbstring
;extension=exif      ; Must be after mbstring as it depends on it
extension=mysqli
;extension=oci8_12c  ; Use with Oracle Database 12c Instant Client
extension=openssl
;extension=pdo_firebird
extension=pdo_mysql
;extension=pdo_oci
extension=pdo_odbc
extension=pdo_pgsql
;extension=pdo_sqlite
extension=pgsql
extension=shmop

; The MIBS data available in the PHP distribution must be installed.
; See http://www.php.net/manual/en/snmp.installation.php
;extension=snmp

extension=soap
extension=sockets
extension=sqlite3
extension=tidy
extension=xmlrpc
extension=xsl
[Date]
; Defines the default timezone used by the date functions
; http://php.net/date.timezone

date.timezone ="PRC"
```

### 三、配置Apache 支持PHP7

1.再次打开conf文件夹下面的httpd.conf文件

2.查找以下关键字，并修改：

<IfModule dir_module>
    DirectoryIndex index.html index.php

</IfModule>

3.在httpd.conf文件最后添加以下内容：
```conf
#php7 support
LoadModule php7_module "E:/mysever/php7/php7apache2_4.dll"
<IfModule php7_module> 
        PHPIniDir "E:/mysever/php7/" 
        AddType application/x-httpd-php .php
        AddType application/x-httpd-php-source .phps
</IfModule>
```

### 四、启动Apache

出现缺少libssh2.dll,libcrypto-1_1-x64.dll,LIBPQ.dll,icuuc60.dll的报错，在Apache 服务目录下编写index.php

添加以下内容：
```php
<?php

echo phpinfo();

?>
```
浏览器访问这个文件，正常运行。

解决以上报错方案：

把PHP7的安装目录：E:\mysever\php7和E:\mysever\php7\ext，添加到环境变量PATH中，重启Apache，不再出现缺少libssh2.dll,libcrypto-1_1-x64.dll,LIBPQ.dll,icuuc60.dll的报错


到这里，我们的Apache服务器配置就完成了，现在可以解析html运行应用了

现在，运行cmd，进入C:\www\Apache24\bin目录，这个目录下的httpd.exe就是服务器的执行程序，根据官网上说的，我们首先把Apache作为应用软件服务安装到系统服务中，运行命令：

httpd -k install -n "ApacheServer"

执行完这条命令后，如果没什么问题，就把Apache服务安装成功了，服务名为：ApacheServer这个我们可以自定义，如果只执行

httpd -k install

这样默认安装Apache服务名为：Apache2.4

如果安装的时候提示，OS 5拒绝服务，AH00369这样的错误，那么原因就是我们没有权限执行操作，那么需要进入C:\Windows\System32目录下，右击cmd.exe选择以管理员方式运行即可，这样就安装成功了

现在运行services.msc就可以看到刚安装好的服务了，并且默认为自动，就是随系统自动启动，不用我们每次再启动了，

如果想手动启动或者关闭或者重启服务器有两种方法，一种是在系统服务中右键进行相应操作，比较简单

另外就是使用命令行进行操作：

启动：httpd -k start -n "ApacheServer"或者默认是httpd -k start

停止：httpd -k stop -n "ApacheServer"或者httpd -k shutdown -n "ApacheServer"

重启：httpd -k restart -n "ApacheServer"

如果需要卸载服务就执行：httpd -k uninstall -n "ApacheServer"

现在，我们访问http://localhost或者http://127.0.0.1如果可以看到 It works!的欢迎页，就是访问到了根目录下的index.html程序，那么Apache的环境就ok了

