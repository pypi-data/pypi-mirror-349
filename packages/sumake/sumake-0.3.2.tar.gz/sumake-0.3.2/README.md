# sumake

[Install](#Install)

[docker-run-remote](#docker-run-remote)




## Introduction

**sumake** is an extension of `make` that simplifies deployment tasks by providing integrated, convenient operations. It makes the deployment process effortless and efficient. With sumake, you can easily build, run, and manage your Docker containers both locally and remotely. The commands are straightforward and designed to save you time and effort.

## Feature

-   **Remote Docker Operations:** Build images and run containers on remote servers seamlessly using ["remote access for Docker"](https://docs.docker.com/engine/daemon/remote-access/) (`docker-build-remote`, `docker-run-remote`).
    -   **Automatic Restart Container:** Automatically build on the server, automatically restart containers. Simple, hassle-free, effortless!
    -   **Simplified Workflow:** Provides intuitive `make` targets abstracting complex Docker commands.
    -   **Environment Variable Integration:** Easily configure builds and runs using environment variables and `.env.make` files.
    -   **Multi-Server Deployment:** Supports one-click deployment to multiple servers, simplifying the process of managing and scaling your applications across different environments.

## Install

1. [Install GNU Make](#install-gnu-make)

2. install pip

3. 
    ```
    pip install sumake -U
    ```

## docker-run-remote

### Example

`.env.make`
```bash
DOCKER_REPOSITORY=sucicada
DOCKER_SERVICE_NAME=japanese-red-blue-book
#DOCKER_SERVICE_PORT=9096
DOCKER_HOST=server.sucicada.me
DOCKER_RUN_OPTS="-p 9086:80"
```
run at the root of the project:
```bash
sumake docker-run-remote
```

it same as :
```bash
DOCKER_HOST=server.sucicada.me \
    docker build -t \
    sucicada/japanese-red-blue-book:latest .

DOCKER_HOST=server.sucicada.me \
    docker stop japanese-red-blue-book 

DOCKER_HOST=server.sucicada.me \
    docker rm japanese-red-blue-book 

DOCKER_HOST=server.sucicada.me \
    docker run -d --name japanese-red-blue-book \
    -p 9086:80 \
    sucicada/japanese-red-blue-book:latest

```

### Prerequisites

-   **Remote Access for Docker:** Ensure that the Docker daemon on the remote server is configured to accept remote connections. https://docs.docker.com/engine/daemon/remote-access/  
    Once configured, you can check the access to the remote server by running:
    ```bash
    sumake docker-info-remote
    ```
    If you see the correct remote docker info, it means the remote access for Docker is working.

### How to use
1. go to the root of the project.

2. Set the environment variables in the `.env.make` file. [Configuration reference](#environment-variables)

3. Run the command:
    ```bash
    sumake docker-run-remote
    ```

4. You can see the remote docker build logs 

### Environment Variables:

- DOCKER_SERVICE_NAME: (required) The name of the docker container.
- DOCKER_SERVICE_PORT: (optional) The port of the docker container. You can set it when you want to expose the port of the docker container. (Equal to docker command: `"-p <port>:<port>"`)
- DOCKER_HOST: (required) The host of the docker server. Remember to set remote access for Docker on the server. [remote access for Docker](https://docs.docker.com/engine/daemon/remote-access/)
- DOCKER_REPOSITORY: (optional) The Docker repository name. Defaults to your Docker Hub username if not set. Used to tag the image (e.g., `<DOCKER_REPOSITORY>/<DOCKER_SERVICE_NAME>:latest`).
- DOCKER_RUN_OPTS: (optional) Additional options for the `docker run` command (e.g., `"-p 8080:80 -v /data:/app/data"`). This allows for flexible configuration like port mapping, volume mounting, etc.


## Install GNU Make

macOS:
```bash
brew install make
```

Ubuntu / Debian / Linux Mint:
```bash
sudo apt-get install make
```

Red Hat / Fedora / CentOS:
```bash
sudo yum install make
```

Arch Linux:
```bash
sudo pacman -S make
```


## dev
(For project development)

make install

pip install . 

*Note: `make install` assumes a local development setup and might require a `Makefile` in the project root.*

## zsh
 ~/.zshrc

```bash
autoload -U compinit
compinit
_sumake() {
_make "$@"
}
compdef _sumake sumake
zstyle ':completion::complete:sumake:*:targets' call-command true
```
