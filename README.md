# Yehpeiwen Detector (業配文是你)
A NLP project for detecting opinion spam.

## /scrapy
We use Scrapy.py to scrape product reviews from Pixnet as our datasets.

### How to use
Make sure you have installed Scrapy.py
```
cd scrapy/
scrapy crawl pixnet -a keyword=<keyword>
```

## /chrome-extension
Yehpeiwen Detector's chrome extension for user client.
***Note that this extension only works on Ptt/Pixnet/Xuite sites because we hardcode DOM query tag names.***

## /aws-lambda
Our serverless back-end codes based on AWS Lambda. This program requires Scikit-learn and Jieba. You may encounter some problem if you package Scikit-learn which is compiled on your computer to AWS Lambda. [For more details](https://github.com/ryansb/sklearn-build-lambda)
