# coding=utf-8
from __future__ import print_function

import sklearn
import json
import jieba
import sys
import io
import re
import string
from math import log

jieba.set_dictionary('dict.txt.big.txt')

def nb(context):
    replace = set([ch for ch in u'[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789’!\"#$%&\\\'「」（）()*+,-./／:;<=>?@，,。?★、…【】《》？“”‘’！[\\\\]^_`{|}~\\n\\t]+'])
    # replace = r'\s[\.\!\/_,$%^*(+\"\'\:\?\]\[]+|[—！，。？、（）：」「)(【】╱；]+\s'
    content = ''.join(context.split())
    wl = jieba.lcut(content)
    content = []
    for w in wl:
        w = ''.join(ch for ch in w if ch not in replace)
        w = ''.join(w.split())
        if w != '':
            content.append(w)
    content = ' '.join(content)

    category = {}
    termNum = 0
    jsonName = 'category.json'
    category = json.loads(io.open(jsonName,'r').read())

    for cate_tmp in category:
        termNum += len(category[cate_tmp]['termf'])

    weightDic = {}
    for cateName in category:
        weightDic[cateName] = 0
    for term in content.split(' '):
        if term == '':
            continue
        for cateName in category:
            if term in category[cateName]['termf']:
                weightDic[cateName] += log(((category[cateName]['termf'][term]+1)*(category[cateName]['doc_prob']))/((category[cateName]['termNum'])+termNum))
            else:
                weightDic[cateName] += log((category[cateName]['doc_prob'])/((category[cateName]['termNum'])+termNum))

    maxCate = max(weightDic.keys(), key=(lambda k: weightDic[k]))
    isSpam = True if maxCate == 'true' else False

    return { 'success': True, 'isSpam': True if maxCate == 'true' else False }

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
    }

def lambda_handler(event, context):
    payload = json.loads(event['body'])
    return respond(None, nb(payload['context']))
