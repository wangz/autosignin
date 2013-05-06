autosignin
==========

use python auto sign webs
the passwd was store in mypasswd.py,please set first

安装pip(python包管理工具)
wget  http://python-distribute.org/distribute_setup.py
sudo python distribute_setup.py
wget  https://github.com/pypa/pip/raw/master/contrib/get-pip.py
sudo python get-pip.py
可以通过pip help来查看帮助。简单用的话只要pip search和pip install就好了。

    pip install chardet
    pip install BeautifulSoup

crontab -e
59 8 * * * python /home/wz/autosignin/moofeel.py &>> /home/wz/autosignin/moofeel.log

