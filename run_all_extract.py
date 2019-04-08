from subprocess import Popen
import shlex

processes = []

for i in range(32):
	processes.append(Popen(shlex.split("python ./feature_extract_crowdsourcing.py " + str(i))))

for p in processes:
	p.wait()
