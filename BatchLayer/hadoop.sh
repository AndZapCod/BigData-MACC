#!/bin/bash
# Andres Zapata
# March 2021 - BigData MACC UR

# En maquina local:
# crear carpeta xmls e introducir los archivos de configuracion .xml
# Ejecutar:
# scp -i file.pem -r xmls/ ubuntu@ec2(...):~/
# scp -i hadoop.sh ubuntu@ec2(...):~/
# scp -i hadoop_ssh.sh ubuntu@ec2(...):~/

# En la instancia AWS EC2:
# chmod +x hadoop.sh
# ./hadoop.sh
 
sudo apt-get update
sudo apt-get -y install ssh pdsh openjdk-8-jdk wget
#wget https://downloads.apache.org/hadoop/common/stable/hadoop-3.3.0.tar.gz
wget https://ftp.wayne.edu/apache/hadoop/common/hadoop-3.3.0/hadoop-3.3.0.tar.gz
tar -xvf hadoop-3.3.0.tar.gz

echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >> hadoop-3.3.0/etc/hadoop/hadoop-env.sh
echo "export HADOOP_HOME=/home/ubuntu/hadoop-3.3.0" >> hadoop-3.3.0/etc/hadoop/hadoop-env.sh
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_HOME=/home/ubuntu/hadoop-3.3.0
echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >> .bashrc
echo "export HADOOP_HOME=/home/ubuntu/hadoop-3.3.0" >> .bashrc
echo "export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin:$JAVA_HOME/sbin" >> .bashrc
source .bashrc

rm ~/hadoop-3.3.0/etc/hadoop/core-site.xml
rm ~/hadoop-3.3.0/etc/hadoop/hdsf-site.xml
rm ~/hadoop-3.3.0/etc/hadoop/mapred-site.xml
rm ~/hadoop-3.3.0/etc/hadoop/yarn-site.xml
sudo cp xmls/*.xml ~/hadoop-3.3.0/etc/hadoop/

sudo mkdir -p /home/ubuntu/bigdata/hadoop/tmp
sudo chmod -R 777 /home/ubuntu/bigdata/hadoop/tmp
sudo chown -R ubuntu:ubuntu /home/ubuntu/bigdata/hadoop/tmp

sudo mkdir -p /home/ubuntu/hadoop/yarn_data/hdfs/namenode
sudo chmod -R 777 /home/ubuntu/hadoop/yarn_data/hdfs/namenode
sudo chown -R ubuntu:ubuntu /home/ubuntu/hadoop/yarn_data/hdfs/namenode

sudo mkdir -p /home/ubuntu/hadoop/yarn_data/hdfs/datanode
sudo chmod -R 777 /home/ubuntu/hadoop/yarn_data/hdfs/datanode
sudo chown -R ubuntu:ubuntu /home/ubuntu/hadoop/yarn_data/hdfs/datanode

ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
ssh localhost
#
# Continuar con hadoop_ssh.sh ...
#