/src: source code.
/tmp: temporary files.
/output: intermediate results and output files.

Requirements:
Python 2.7.8
NTLK package & rdflib, easy to install with pip.
Standford NER Tagger

Execute:
I write a shell script in /src. It downloads the needed Stanford Packages to /src first. Then execute the source code to get the results. Just type: ./run.sh.

Source code:
prepare.py: prepare needed data
player2nation.py: query player's information about nationality from DBpedia
team2stdium.py: query team's information about stadium from DBpedia
main.py: answer the given questions

q1.py: answer question 1
q2.py: answer question 2
q3.py: answer question 3
q4.py: answer question 4
q5.py: answer question 5
