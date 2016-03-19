wget http://nlp.stanford.edu/software/stanford-parser-full-2015-04-20.zip
wget http://nlp.stanford.edu/software/stanford-ner-2014-06-16.zip
unzip stanford-parser-full-2015-04-20.zip
unzip stanford-ner-2014-06-16.zip

export STANFORDTOOLSDIR=$HOME/Coding/Course/CMPUT690/Assignment2/src

export CLASSPATH=$STANFORDTOOLSDIR/stanford-ner-2014-06-16/stanford-ner.jar:$STANFORDTOOLSDIR/stanford-parser-full-2015-04-20/stanford-parser.jar:$STANFORDTOOLSDIR/stanford-parser-full-2015-04-20/stanford-parser-3.5.2-models.jar

export STANFORD_MODELS=$STANFORDTOOLSDIR/stanford-ner-2014-06-16/classifiers

python split.py
python ner.py
python extraction.py
python cluster.py
