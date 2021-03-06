#!/usr/bin/env python3
import pika
import sys
import random
import json

def main():
    if(len(sys.argv) < 2):
        print("usage: ./server.py [input-file.txt]")
        sys.exit(1)

    mq_queue = "task_queue2"

    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=mq_queue, durable=True)

    try:
        with open(sys.argv[1]) as f:
            servers = [line.rstrip().split(":") for line in f]
            random.shuffle(servers)
    except:
        print("Error reading file. Did you give me the right location?")
        sys.exit(1)

    servers_len = len(servers)
    print("[-] Started sending to queue")

    while len(servers) > 0:
        server = servers[0]
        channel.basic_publish(exchange='',
                            routing_key=mq_queue,
                            body=json.dumps(server),
                            properties=pika.BasicProperties(
                                delivery_mode = 2, # make message persistent
                            ))
        if len(servers) % 512 == 0:
            print("[-] Progress {:.3f}% [{}/{}]".format(
                ((servers_len-len(servers))/servers_len)*100, 
                servers_len-len(servers), 
                servers_len
            ))
        servers.pop(0)

    print("[-] [finished] Progress 100% [{}/{}]".format(servers_len, servers_len))
    connection.close()

if __name__ == "__main__":
	main()
