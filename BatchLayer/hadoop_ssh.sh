#!/bin/bash
# Andres Zapata
# March 2021 - BigData MACC UR

# En la instancia AWS EC2 conectado a ssh localhost
# chmod +x hadoop_ssh.sh
# ./hadoop_ssh.sh

# Creditos a Samuel en Slack
pdsh -q -w localhost
export PDSH_RCMD_TYPE=ssh

hdfs namenode -format
start-dfs.sh
start-yarn.sh
jps
