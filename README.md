# ftpscout

> Scanning ftps for anonymous access

![ftpscout](https://i.imgur.com/CohQgcC.png)

### Installation
ftpscout uses RabbitMQ to manage the queues

###OSX

```sh
$ brew install rabbitmq
$ /usr/local/sbin/rabbitmq-server
```

###Linux

apt based

```sh
$ echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee /etc/apt/sources.list.d/rabbitmq.list
$ sudo apt-get update
$ sudo apt-get install rabbitmq-server
$ service rabbitmq-server start
```

rpm based

```sh
$ yum install erlang
$ rpm --import https://www.rabbitmq.com/rabbitmq-release-signing-key.asc
$ yum install rabbitmq-server-3.6.2-1.noarch.rpm
$ service rabbitmq-server start
```

Arch linux
```sh
$ sudo pacman -S rabbitmq
$ systemctl start rabbitmq-server
```

Next, you need to clone this repo
```sh
$ git clone git://github.com/RubenRocha/ftpscout.git
```

install python dependencies
```sh
$ pip3 install -r requirements.txt
```

### usage
The main script is ftpscout.py, if you only want to use one instance of ftpscout (e.g no multi-processing), run this
```sh
$ python3 ftpscout.py log.txt
```

if you want multi-processing, use our launch.sh
```sh
$ ./launch.sh [number-of-threads] [logfile]
```

Next, you need to send some ip's to the queue
You can feed a list in ip:port format (or just ip and it will assume port 21) or, hostname/hostname:ip
```sh
$ python3 server.py list.txt
```

It also includes a tool for adding ip ranges (CIDR) easily
```sh
$ ./cidr_scout.sh 192.168.1.0/24
$ ./cidr_scout.sh 192.168.1.0/24 127.0.0.0/24
```
