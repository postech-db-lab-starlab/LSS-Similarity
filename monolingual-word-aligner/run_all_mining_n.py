from subprocess import Popen
import shlex

processes = []

for i in range(32):
	processes.append(Popen(shlex.split("python ./Mining_words_snm_n.py " + str(40000+i) + " " + str(i))))

for p in processes:
	p.wait()
