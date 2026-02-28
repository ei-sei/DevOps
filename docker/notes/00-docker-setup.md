The following instructions show how to install docker on Fedora 43. For other OS, please refer to the official docker documentation

https://docs.docker.com/engine/install/fedora/#set-up-the-repository

```bash
# 1. Remove conflicting packages
sudo dnf remove docker docker-client docker-client-latest docker-common \
  docker-latest docker-latest-logrotate docker-logrotate docker-selinux \
  docker-engine-selinux docker-engine

# 2. Add the official Docker repo (dnf5 syntax for Fedora 41+)
sudo dnf config-manager addrepo --from-repofile https://download.docker.com/linux/fedora/docker-ce.repo

# 3. Install Docker Engine
sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 4. Start and enable the daemon
sudo systemctl enable --now docker

# 5. Verify
sudo docker run hello-world
```


If Docker keeps requesting sudo permissions to run commands, to make your life easier you can add your user to the Docker group
```bash
# Add your user to Docker group
sudo usermod -aG docker $USER

# Apply changes without rebooting
newgrp docker

# Verify
docker ps

```