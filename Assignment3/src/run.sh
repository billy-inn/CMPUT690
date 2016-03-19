# Downlaod Stanford NER Tagger to /usr/share
#wget http://nlp.stanford.edu/software/stanford-ner-2014-06-16.zip
#unzip stanford-ner-2014-06-16.zip
#mv stanford-ner-2014-06-16 stanford-ner

# Execute the source code and get the result
python prepare.py
python player2nation.py
python team2stadium.py
python main.py
