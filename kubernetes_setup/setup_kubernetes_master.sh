#!/usr/bin/env bash

# https://stackoverflow.com/questions/59895/get-the-source-directory-of-a-bash-script-from-within-the-script-itself
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

./$(DIR)/install_kubernetes.sh

sudo kubeadm init --pod-network-cidr=10.244.0.0/16 | tee $(DIR)/temp.out
echo "#!/usr/bin/env bash" > $(DIR)/add_node_to_cluster.sh
sed ':loop /[^\\]\\$/N; s/\\\n//; t loop' $(DIR)/temp.out | grep "." | tail -n 1 >> $(DIR)/add_node_to_cluster.sh
chmod +x $(DIR)/add_node_to_cluster.sh
rm $(DIR)/temp.out

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
