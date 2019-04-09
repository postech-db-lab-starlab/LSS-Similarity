from subprocess import Popen
import shlex

processes = []

for i in range(16):
	processes.append(Popen(shlex.split("python ./Mining_words.py " + str(i))))

for p in processes:
	p.wait()

f = open("Mined_words.sql.txt", "w")
for i in range(16):
    nf = open("Mined_words/Mined_words.sql_" + str(i) + ".txt", "r")
    for l in nf:
        f.write(l)
f.close()

f = open("Mined_words.nl.txt", "w")
for i in range(16):
    nf = open("Mined_words/Mined_words.nl_" + str(i) + ".txt", "r")
    for l in nf:
        f.write(l)
f.close()
