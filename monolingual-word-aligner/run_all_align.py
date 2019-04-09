from subprocess import Popen
import shlex

processes = []

for i in range(16):
	processes.append(Popen(shlex.split("python ./Batch_aligner.py " + str(i))))

for p in processes:
	p.wait()
