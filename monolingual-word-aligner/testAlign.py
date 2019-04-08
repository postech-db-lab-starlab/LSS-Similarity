from aligner import *



while True:
  sentence1 = raw_input()
  sentence2 = raw_input()
  alignments = align(sentence1, sentence2)
  print alignments[0]
  print alignments[1]

# aligning strings (output indexes start at 1)
sentence1 = "SELECT department, MAX(salary) AS Highest salary FROM employees GROUP BY department HAVING MAX(salary) > 50000;"
sentence2 = 'select department, MAX of salary of employees for each department that MAX of salary is larger than 50000'

alignments = align(sentence1, sentence2)

print alignments[0]
print alignments[1]
print


# aligning sets of tokens (output indexes start at 1)
sentence1 = ['Four', 'men', 'died', 'in', 'an', 'accident', '.']
sentence2 = ['4', 'people', 'are', 'dead', 'from', 'a', 'collision', '.']

alignments = align(sentence1, sentence2)

print alignments[0]
print alignments[1]

