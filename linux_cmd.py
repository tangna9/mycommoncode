# -*- coding: UTF-8 -*-'
import paramiko
from fg_func import my_exception as my_e

def ssh(host, port, user, password, cmd):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host,int(port),user,password)
    stdin,stdout,stderr = ssh.exec_command(cmd)
    str1 = stdout.readlines()
    return str1

def ssh2(host, port, user, password, cmd):

    try:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, int(port), user, password)
        except Exception, e:
            print e
        stdin, stdout, stderr = ssh.exec_command(command=cmd, timeout=20)
        str_out = stdout.readlines()
        str_err = stderr.readlines()
        if stderr:
            raise my_e.LinuxCommException(str_err)
    finally:
        ssh.close()
    return str_out