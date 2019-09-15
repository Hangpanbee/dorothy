from textblob import TextBlob
from flask import Flask, render_template, request, jsonify

def sentimental_analysis(message):
    a = TextBlob(message).sentiment.polarity
    b = TextBlob(message).sentiment.subjectivity
    return a, b


print(sentimental_analysis('I feel really really sad'))

