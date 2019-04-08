from subprocess import Popen
import shlex

processes = []

for i in range(32):
	processes.append(Popen(shlex.split("python ./Batch_aligner_sqlnlmatch.py " + str(i))))

for p in processes:
	p.wait()
