#!/bin/bash
set -e -x

function amd_terraform_install() {
    curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add -
    apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
    apt-get update
    apt-get install -y terraform
}
function arm_terraform_install() {
    curl https://releases.hashicorp.com/terraform/1.9.0/terraform_1.9.0_linux_arm64.zip -o "/tmp/terraform.zip"
    unzip "/tmp/terraform.zip" -d /tmp
    mv "/tmp/terraform" "/usr/local/bin/terraform"
    rm "/tmp/terraform.zip"
}

function amd_awscli_install() {
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip"
    unzip "/tmp/awscliv2.zip" -d "/tmp"
    /tmp/aws/install
    rm -rf "/tmp/awscliv2.zip" "/tmp/aws"
}
function arm_awscli_install() {
    curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "/tmp/awscliv2.zip"
    unzip "/tmp/awscliv2.zip" -d "/tmp"
    /tmp/aws/install
    rm -rf "/tmp/awscliv2.zip" "/tmp/aws"
}

function amd_ssm_plugin_install() {
    curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o "/tmp/session-manager-plugin.deb"
    dpkg -i "/tmp/session-manager-plugin.deb"
    rm "/tmp/session-manager-plugin.deb"
}
function arm_ssm_plugin_install() {
    curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_arm64/session-manager-plugin.deb" -o "/tmp/session-manager-plugin.deb"
    dpkg -i "/tmp/session-manager-plugin.deb"
    rm "/tmp/session-manager-plugin.deb"
}

arch=$(uname -m)
case "$arch" in
    x86_64 | i686 | i386 )
        amd_terraform_install
        amd_awscli_install
        amd_ssm_plugin_install
        ;;
    arm64 | aarch64 )
        arm_terraform_install
        arm_awscli_install
        arm_ssm_plugin_install
        ;;
    * )
        echo "Unsupported CPU architecture: $arch"
        exit 1
        ;;
esac
