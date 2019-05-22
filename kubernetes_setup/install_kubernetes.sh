#!/usr/bin/bash

sudo apt update && sudo apt -y upgrade
sudo apt -y install apt-transport-https
sudo apt -y install docker.io

sudo systemctl start docker
sudo systemctl enable docker

curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add

sudo apt-add-repository -y "deb http://apt.kubernetes.io/ kubernetes-xenial main"

sudo apt -y install kubeadm

sudo swapoff -a

echo "Disabling swap in fstab"
sudo cp /etc/fstab /etc/fstab.bak
sudo sed -e '/.*swap.*/s/^/#/g' -i /etc/fstab
