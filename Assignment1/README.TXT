/src: source code.
/data: processed data.
/utils: auxiliary scripts and data.
/model: saved word2vec model
/output: output file.

Requirements:
Python 2.7.8
NLTK package, easy to install with pip.
Wordnet corpus in NLTK, use nltk.download() in python shell to download.
Stanford NER tagger in NLTK, see http://textminingonline.com/how-to-use-stanford-named-entity-recognizer-ner-in-python-nltk-and-other-programming-languages for reference. In my implementation, the path is /src.

Execute:
python split.py		% preprocess the data
python baseline.py	% get the baseline output
python output.py	% get the final output
python CR.py		% get the coreference resolution output

I also write a shell script. It downloads the Stanford NER to /src first and then execute the source code. Just type: ./run.sh.
