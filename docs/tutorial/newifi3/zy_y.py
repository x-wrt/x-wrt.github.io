#-*- coding:utf8 -*-
import paramiko
import urllib.request
import time
import urllib
import requests
import webbrowser
import socket


#变量配置
down ="./eeprom.bin"
router = "http://192.168.99.1"
eeprom = "http://192.168.99.1/eeprom.bin"
openssh = "http://192.168.99.1/newifi/ifiwen_hss.html"
#open = "http://192.168.99.1"

print()
print("NEWIFI3 一键刷入Breed")
print()
print("CopyRight By Zy143L")
print("Breed CopyRight Hackpascal")
print()
print("正在侦测路由器")
print()

try:
    code = requests.get(openssh, timeout=5).status_code
    #print(r)
    #code = r
except requests.exceptions.ConnectTimeout:
    print("无法侦测到路由器"),print("请检查路由器状态")
    time.sleep(1)
    print("回车退出程序")
    input()
    exit()


def shizuku ():
    while True:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname="192.168.99.1", port=22, username="root", password=input("路由器密码: "))
            break
        except paramiko.ssh_exception.AuthenticationException:
            print("路由器密码错误 请重试"), print()
            shizuku()
    # ssh.connect(hostname="127.0.0.1",username="shizuku",password="shizuku")
    print(), print("路由器连接成功")
    stdin, stdout, stderr = ssh.exec_command("wget https://gitee.com/zy143l/OpenWRT/raw/master/shizuku.ko")
    result = stdout.read()
    print(stdout.read(), stderr.read())
    stdin, stdout, stderr = ssh.exec_command("md5sum shizuku.ko | awk '{print $1}'")
    ko_md5sum = stdout.read()
    print(ko_md5sum, stderr.read())
    if (b'733b6977ee83b529b733df199b7cd2fe\n' != ko_md5sum):
        print("请尝试切换到 https://raw.githubusercontent.com/chinapedia/OpenWRT/master/shizuku.ko")
        exit(1)
    stdin, stdout, stderr = ssh.exec_command("Z_eeprom=`cat /proc/mtd | grep Factory | cut -b 1-4` && echo ${Z_eeprom}")
    print(stdout.read(), stderr.read())
    cmd = 'Z_eeprom=`cat /proc/mtd | grep Factory | cut -b 1-4` && dd if=/dev/${Z_eeprom} of=/tmp/eeprom.bin'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(cmd, ":", stdout.read(), stderr.read())
    stdin, stdout, stderr = ssh.exec_command('ln -s /tmp/eeprom.bin /www/eeprom.bin')
    print(stdout.read(), stderr.read())

    print()
    print("EEPROM备份成功 开始下载")
    urllib.request.urlretrieve(eeprom, down)
    time.sleep(1)
    print()
    print("下载完成: "+down)
    print()
    print("回车开始刷机")
    input()
    stdin, stdout, stderr = ssh.exec_command("insmod shizuku.ko")
    result = stdout.read()
    #ssh.close()
    print(), print("成功")
    print("CopyRight By Zy143L")
    time.sleep(5)
    exit()

if code == 404:
    time.sleep(1)
    print("路由器配置异常!"),print("请在浏览器打开的配置路由器"),print("即将通过浏览器打开配置页面"),print("请配置好路由器后再次打开本程序")
    print("回车确定")
    input()
    #webbrowser.open(router, new=0, autoraise=True)
    webbrowser.open_new(router)
    #webbrowser.open_new_tab(router)
    exit()
else:
    if code == 200:
        ###time.sleep(1)
        print("路由器配置正常")
        print()
        print("正在检测SSH服务")
        print()
        time.sleep(1)
        try:
            zy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            zy.settimeout(3)
            zy.connect(('192.168.99.1', 22))
            zy.close()
            print("SSH服务正常")
            print()
            shizuku()
            exit(0)
        except ConnectionRefusedError:
            print("SSH服务异常")
            print()
            print("正在开启SSH服务")
            print()
            while True:
                try:
                    postData = "{'id': '1', 'jsonrpc': '2.0', 'method': 'call', 'params': ['00000000000000000000000000000000', 'xapi.basic', 'open_dropbear', {}]}"
                    ubus = "http://192.168.99.1/ubus"
                    response = requests.post(ubus, data=postData, timeout=4)
                    break
                except requests.exceptions.ConnectionError:
                    print("SSH启动失败!"),print("请检查路由器状态"),print("回车退出")
                    input(),time.sleep(3)
                    exit()


            #print(response.text)
            print("SSH服务开启成功")
            print()
            shizuku()


        #webbrowser.open(openssh, new=0, autoraise=True)
        ###
        #webbrowser.open_new_tab(openssh)







