from subprocess import Popen
import shlex

processes = []

for i in range(32):
	processes.append(Popen(shlex.split("python ./corenlp.py -p " + str(40000+i))))

for p in processes:
	p.wait()
