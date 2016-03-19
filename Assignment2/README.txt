/src: source code.
/data: processed data.
/output: intermediate results and output file.

Requirements:
Python 2.7.8
NLTK package, easy to install with pip.
Stanford NER Tagger & Stanford Parser

Execute:
I write a shell script in /src. It downloads the needed Stanford Packages to /src first. And then set the environment variables. Finally execute the source code to get the results. Just type: source ./run.sh (Note: Need to use command 'source' in order to set the enviroment variables!) 

Source code:
split.py: Preprocess
ner.py: Name Entity Recognition
extraction.py: Extract Raw Relations via Dependency Tree
cluster.py: Cluster the Raw Relations into Formal Relations
