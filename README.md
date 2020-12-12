
cp /etc/ssh/sshd_config /etc/ssh/sshd_config_tmp to prevent misconfiguration in ssh
Run app.py

commands:

getting option value:
    ssh.getval <option>

setting value:
    ssh.setval <option>:<value>

getting all configs:
    ssh.configs

write config to file:
    ssh.apply

getting docker version:
    docker.ver

getting docker build number:
    docker.build