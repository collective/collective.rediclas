Introduction
============

The aim of rediclas is to make tagging simpler. It tries to achive this
with a Naïve Bayesian Text Classifier which is persisted on Redis.
The Name stands for 'a ridiculously naive bayesian classifier on redis'.

Configuration
=============

Redis
------

Connfigure the parameters that are necessary to connect to your Redis
server.

Configure which contenttypes should be clasified and which keywords to
exclude from the classification.

Stopwords
----------

To avoid too much noise in your classifiers you should specify stopwords
for your language. Stopword lists are available for download so just search
for it. The stopword list does not have to be in a specific format as
it will be preprocessed so you can just copy and paste it into the text field.

The stopwords are stored in redis.

Training
---------

Before you can get any recommendations you have to train the Bayesian
Classifier. You can either do this in the controlpanel, or you can
append `@@rediclas-train.html` to any folder, topic or collection in
your site. In case of a Folder all content in its path, on a Topic or
Collection all content matching the criteria will be searched.
