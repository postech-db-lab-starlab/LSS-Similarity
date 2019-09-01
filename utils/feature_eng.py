import random

new_f = open('data/new_faa.txt', 'w')
f = open('data/feature_answer_all.txt')

n_t = 0
n_f = 0
feats = []
for l in f:
    if n_t >= 250 and n_f >= 250:
        break
    parts = l.strip().split()
    target = int(float(parts[-1]))
    if target == 1:
        if n_t < 250:
            feats.append(l)
            n_t += 1
    if target == 0:
        if n_f < 250:
            feats.append(l)
            n_f += 1

random.shuffle(feats)

for l in feats:
    new_f.write(l)