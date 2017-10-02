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

## Install/Upgrade 'ansible' via 'pip'
`sudo pip install --user --upgrade ansible`

## Verification
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
Darwin ovpn-205-30.brq.redhat.com 16.7.0 Darwin Kernel Version 16.7.0: Thu Jun 15 17:36:27 PDT 2017; root:xnu-3789.70.16~2/RELEASE_X86_64 x86_64
```

# Create python2.7 virtual environment for Ansible
`virtualenv --python=python2.7 .venv`

# Activate python2.7 virtual environment
`source .venv/bin/activate`

# Export AWS environment variabled
- `export AWS_ACCESS_KEY_ID=<your-aws-access-key-id>`
- `export AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key>`

# Clone ansible repository locally
`git clone git@github.com:vchepeli/aws-performance.git`

# Change directory to aws-performance
`cd aws-performance`

# Create your secret password for sensitive informatino
`openssl rand -base64 8 > .password`

# Creare secret.yml file for Jenkins credentials
`ansible-vault --vault-password-file=.password create secret.yml`

```
vault_jenkins_username: <your-kerberos-username>
vault_jenkins_password: <your-kerberos-password>
vault_jenkins_url: <jenkins master web console>
```

# Update hosts inventory file with your local user name
`my  ansible_host=127.0.0.1 ansible_user=<your-local-username> ansible_connection=local`

# Generate SSH keys for AWS and Jenkins
- `ssh-keygen -t rsa -b 4096 -C "<your-email-address>" -f ~/.ssh/ec2.centos -q -N ""`
- `ssh-keygen -t rsa -b 4096 -C "<your-email-address>" -f ~/.ssh/ec2.jenkins -q -N ""`

# Run Ansible playbook
`ansible-playbook -i hosts play.yml -v --vault-password-file .password --ask-become-pass`