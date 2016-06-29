#!/usr/bin/env python3
import pika
import sys
import random
import json

mq_queue = "task_queue2"

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue=mq_queue, durable=True)

with open(sys.argv[1]) as f:
    servers = [line.rstrip().split(":") for line in f]
    random.shuffle(servers)

while len(servers) > 0:
    server = servers[0]
    channel.basic_publish(exchange='',
                        routing_key=mq_queue,
                        body=json.dumps(server),
                        properties=pika.BasicProperties(
                            delivery_mode = 2, # make message persistent
                        ))
    print(" [-] Sent {} to queue".format(server))
    servers.pop(0)
    
connection.close()
