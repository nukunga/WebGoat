import subprocess
import os

# 최신 업데이트 명령어 실행
subprocess.run(["sudo", "yum", "-y", "update"])

# wget 명령어 실행
subprocess.run(["wget", "-q", "https://github.com/zaproxy/zaproxy/releases/download/v2.14.0/ZAP_2.14.0_Linux.tar.gz"])

# tar 명령어 실행
subprocess.run(["tar", "-zxvf", "ZAP_2.14.0_Linux.tar.gz"])

# rm 명령어 실행
subprocess.run(["rm", "ZAP_2.14.0_Linux.tar.gz"])

# ZAP_2.14.0 디렉토리로 이동
subprocess.run(["cd", "ZAP_2.14.0"])

# cp 명령어로 파일을 /home/ec2-user/ZAP_2.14.0/ 로 복사
subprocess.run(["cp", "-r", "./ZAP_2.14.0/", "/home/ec2-user/ZAP_2.14.0/"])

# cd 명령어 실행
subprocess.run(["chmod", "+x", "./ZAP_2.14.0/zap.sh"], cwd="/home/ec2-user")
subprocess.run(["sudo", "yum", "-y", "install", "git"], cwd="/home/ec2-user")
subprocess.run(["pip3", "install", "--upgrade", "git+https://github.com/Grunny/zap-cli.git"], cwd="/home/ec2-user")

# chmod 명령어 실행
subprocess.run(["chmod", "+x", "./zap.sh"])

# java17 설치 명령어 실행
subprocess.run(["sudo", "yum", "-y", "install", "java-17-amazon-corretto"])
subprocess.run(["sudo", "yum", "-y", "install", "java-17-amazon-corretto-devel"])

# Git 설치 명령어 실행
subprocess.run(["sudo", "yum", "-y",  "install", "git"])

# pip3 install 명령어 실행
subprocess.run(["pip3", "install", "--upgrade", "git+https://github.com/Grunny/zap-cli.git"])

# zap-cli를 ZAP_2.14.0/ 으로 복사
subprocess.run(["cp", "/home/ec2-user/.local/bin/zap-cli", "/home/ec2-user/ZAP_2.14.0"])