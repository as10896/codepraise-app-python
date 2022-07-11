# Prerequisite
## Install Docker
Make sure you have the latest version of <a href="https://www.docker.com/get-started" target="_blank">Docker 🐳</a> installed on your local machine.

## Set up session secret for cookie-based session management
Put your session secret key under `config/secrets/<env>/SESSION_SECRET`.

Or just set the environment variable `SESSION_SECRET`:
```shell
export SESSION_SECRET=<your secret>
```

One way to generate a key is to use `openssl rand`
```shell
openssl rand -hex 32
```
