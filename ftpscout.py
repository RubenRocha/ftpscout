#!/usr/bin/env python3
# ftpscout v.0.1
#
# notice: this requires RabbitMQ.
# to add to the queue simply pass a text file to server.py containing the hosts in
# ip:port or hostname:port format, seperated by a newline
#
# usage: ./ftpscout.py [logfile.txt]
# usage (threaded): ./launch.sh [number of threads] [logfile.txt]
# 
# This project is licenced under the GNU GPLv3
# GitHub: https://github.com/RubenRocha/ftpscout

import ftplib
import os
import socket
import sys
import colorama
import random
import pika
import time
import json
from urllib.parse import urlparse
from random import shuffle

from colorama import init, Fore, Back, Style
from datetime import datetime

init()

log_file = ""
log_strs = []
users = ["anonymous"]
passwords = ["guest","anonymous"," ", ""]

mq_queue="task_queue2"

def log(color, m_str, log_this=True):
	global log_file
	pid = str(os.getpid())
	print(Fore.MAGENTA + "[*] [thread {}] {} {} {}".format(Fore.GREEN + pid, color, m_str, Style.RESET_ALL))
	if len(log_file) > 0 and log_this:
		log_strs.append(m_str)
		

def save_log():
	global log_strs
	with open(log_file, "a+") as myfile:
		myfile.write('\n'.join(log_strs))
	log_strs = []

def color(clr, strp):
	return "{}{}{}".format(clr,strp,Style.RESET_ALL)

def try_login(custom_users, custom_passwords, host, port):
	for user in custom_users:
		for password in custom_passwords:
			try:
				con = ftplib.FTP(timeout=3.5)
				con.connect(host, port)
				ans = con.login(user,password)
				if "230" in ans:
					anon_login = "Success ({} - {})".format(user, password)
					dir_listing = get_directory_listing(con)
					return (anon_login, dir_listing)
				else:
					con.quit()
					con.close()
					continue
			except socket.timeout:
				anon_login = "Disallowed/Timed out"
				con.quit()
				con.close()
				return (anon_login, None)
			except Exception as e:
				anon_login = "Disallowed/Error"
				con.quit()
				con.close()
	return (anon_login, None)

def get_banner(host,port):
	socket.setdefaulttimeout(3.5)
	s = socket.socket()
	try:
		s.connect((host, port))
		ans = s.recv(1024)
		s.close()
		ans = ans.decode().rstrip().replace("\r", "").replace("\n", "\n\t")
		if len(ans) == 0:
			return "Empty"
		else:
			return ans
	except Exception as e:
		return "Error/Can't connect"

def get_directory_listing(ftp_con):
	try:
		files = ftp_con.nlst()
		if "." in files: files.remove(".")
		if ".." in files: files.remove("..")

		rnd_files = random.sample(set(files), 3)
		
		return "{} files listed - sample of files: {}".format(len(files), rnd_files)
	except ftplib.error_perm as resp:
		if "550" in resp:
			return "No files"
	finally:
		con.quit()
		con.close()

def differenciate_list(custom_list, real_list, l_type):
	for k,i in enumerate(custom_list[:]):
		if k >= len(real_list):
			log(Fore.MAGENTA, "Added {} '{}' to current domain".format(l_type, custom_list[k]), log_this=False)

def port_check(host, port):
	try:
		socket.setdefaulttimeout(0.650)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		res = s.connect_ex((host,port))
		s.close()
		return True if res == 0 else False
	except Exception as e:
		return False

def scan(host,port=21):
	try:
		results = []
		custom_users = list(users)
		custom_passwords = list(passwords)

		if not port_check(host,port):
			log(Fore.RED, "Port {} seems to be closed for {}. Skipping...".format(port, color(Fore.YELLOW, host)), log_this=False)
			return

		try:
			socket.inet_aton(host)
		except socket.error:
			nhost = host.replace("www.", "")
			urlp = urlparse("//" + nhost)
			custom_users.append("anonymous"+"@"+nhost)
			custom_users.append(urlp.netloc)
			custom_users.append(nhost.split(".")[0])
			custom_passwords.append(nhost.split(".")[0])
		

		differenciate_list(custom_users, users, "username")
		differenciate_list(custom_passwords, passwords, "password")

		log(Fore.CYAN, "Scanning {}:{} - please wait.".format(host,port), log_this=False)

		anon_login,dir_listing = try_login(custom_users, custom_passwords, host, port)
		banner = get_banner(host, port)

		if "Timed out" in anon_login:
			log(Fore.RED, "Results for {}:{} \r\n\t-> Timed out".format(host,port))
			return

		if "Error" in anon_login:
			log(Fore.RED,	("Results for {}:{} \r\n" +
						"\t-> Anonymous access: {}\r\n" +
						"\t-> FTP banner: {}\n")
						.format(host,port,anon_login,banner)
			)
			return
		
		log_color = Fore.RED if "Disallowed" in anon_login else Fore.GREEN

		log(log_color,	("Results for {}:{} \r\n" +
						"\t-> Anonymous access: {}\r\n" +
						"\t-> FTP banner: {}\r\n" + 
						"\t-> Dir listing: {}\n")
						.format(host,port,anon_login,banner,dir_listing)
			)

	except(KeyboardInterrupt):
		log(Fore.RED, "Interrupted. Later!", log_this=False)
		sys.exit()

def callback(ch, method, properties, body):
	global log_strs
	server = json.loads(body.decode('utf-8'))
	scan(server[0], 21 if 1 <= len(server) else server[1])
	save_log()
	ch.basic_ack(delivery_tag = method.delivery_tag)

def mq_worker():
	try:
		connection = pika.BlockingConnection(pika.ConnectionParameters(
			host='localhost'))
		channel = connection.channel()

		channel.queue_declare(queue=mq_queue, durable=True)

		channel.basic_qos(prefetch_count=1)
		channel.basic_consume(callback,
							queue=mq_queue)

		channel.start_consuming()
	except Exception as e:
		log(Fore.BLUE, "Waiting for data from queue...", log_this=False)
		mq_worker()


def main():
	global log_file
	log(Fore.YELLOW, "Loaded usernames: {}".format(users))
	log(Fore.YELLOW, "Loaded passwords: {}\n".format(passwords))
	
	log_file = sys.argv[1] if len(sys.argv) >= 2 else "log.txt"

	mq_worker()


	
if __name__ == "__main__":
	main()
