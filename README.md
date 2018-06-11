# To follow this article, you will need the following:
- python2.7 latest installed on your system
- root user with sudo privileges

# Install Tooling on your local machine

## Install the Command Line Developer Tools for OS X
`sudo xcode-select --install`

## Install 'pip'
`sudo easy_install pip`

## Verify the 'pip' command is now in our PATH
`pip --version`

## Upgrade 'pip' version to latest
`sudo pip install --user --upgrade pip`

## Install/Upgrade 'ansible' to latest
`sudo pip install --user --upgrade ansible`

## Verification of Ansible installation
By default, we don't have an existing Ansible Inventory, but we can run ansible with localhost as the target

`ansible localhost -m ping`
```
localhost | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```
`ansible localhost -m setup -a 'filter=ansible_distribution'`
```
localhost | SUCCESS => {
    "ansible_facts": {
        "ansible_distribution": "MacOSX"
    },
    "changed": false
}
```

`ansible localhost -a 'uname -a'`
```
localhost | SUCCESS | rc=0 >>
Darwin vchepeli-OSX.local 17.5.0 Darwin Kernel Version 17.5.0: Fri Apr 13 19:32:32 PDT 2018; root:xnu-4570.51.2~1/RELEASE_X86_64 x86_64
```

# Create Virtual Environment(Optional)
This does a user installation to prevent breaking any system-wide packages

## Create python2.7 virtual environment for Ansible
`virtualenv --python=python2.7 .venv`

## Activate python2.7 virtual environment
`source .venv/bin/activate`

# Add cloud ENVs to yous shell
## Export Openstack ENVs
`chmod +x <project-name>-openrc.sh`
`./<project-name>-openrc.sh`

## Export AWS ENVs
- `export AWS_ACCESS_KEY_ID=<your-aws-access-key-id>`
- `export AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key>`

# Clone ansible repository locally
`git clone git@github.com:vchepeli/aws-performance.git && cd aws-performance`

# Create your secret password for sensitive informatino
`openssl rand -base64 15 > .password`

# Creare secret.yml file for Jenkins credentials
`ansible-vault --vault-password-file=.password create secret.yml`

```
vault_jenkins_username: <your-username>
vault_jenkins_password: <your-password>
vault_jenkins_url: <jenkins-master-url>
```

# Update hosts inventory file with your local user name(Optional)
`my  ansible_host=127.0.0.1 ansible_user=<your-local-username> ansible_connection=local`
 

# Generate SSH keys for AWS EC2/Openstack and Jenkins
- `ssh-keygen -t rsa -b 2048 -C "<your-email-address>" -f ~/.ssh/ec2.centos -q -N ""`
- `ssh-keygen -t rsa -b 2048 -C "<your-email-address>" -f ~/.ssh/ec2.jenkins -q -N ""`

# Run Ansible playbook
`ansible-playbook -i hosts play.yml -v --vault-password-file .password --ask-become-pass`
