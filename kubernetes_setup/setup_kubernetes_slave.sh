#!/usr/bin/env bash

# https://stackoverflow.com/questions/59895/get-the-source-directory-of-a-bash-script-from-within-the-script-itself
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"


$DIR/install_kubernetes.sh
echo Enter the master node address:
read MASTER_NODE_ADDRESS
echo Enter the master node username:
read USERNAME

scp ${USERNAME}@${MASTER_NODE_ADDRESS}:${DIR}/add_node_to_cluster.sh ${DIR}
${DIR}/add_node_to_cluster.sh
