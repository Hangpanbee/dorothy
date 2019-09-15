import random
import config
import tensorflow as tf
from flask import Flask, render_template, request, jsonify
import azure.cognitiveservices.speech as speechsdk
from voice import resultCheck
from textblob import TextBlob
import time
from bs4 import BeautifulSoup
import requests
import json
import pickle
from graph_Utils import sentence_to_seq, make_pred
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)
sys.path.append('..')


vocabs_to_index = pickle.load(open("vocab2index.p", "rb"))
index_to_vocabs = pickle.load(open("index2vocab.p", "rb"))
batch_size = config.BATCH_SIZE
model_dir = config.MODEL_DIR
save_path = config.SAVE_PATH

loaded_graph = tf.Graph()
sess = tf.InteractiveSession(graph=loaded_graph)
save_path = model_dir+'/'+save_path
dir(tf.contrib)
loader = tf.train.import_meta_graph(save_path + '.meta')
loader.restore(sess, save_path)
input_data = loaded_graph.get_tensor_by_name('input:0')
logits = loaded_graph.get_tensor_by_name('predictions:0')
input_data_len = loaded_graph.get_tensor_by_name('input_len:0')
target_data_len = loaded_graph.get_tensor_by_name('target_len:0')
keep_prob = loaded_graph.get_tensor_by_name('keep_prob:0')


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat')
def chat():
    return render_template('chatcopy.html', myfunction=resultCheck)


@app.route('/getaudio')
def getaudio():
    return(resultCheck)


'''
@app.route('/audio', methods = ['POST'])
def get_audio():
    speech_key, service_region = "e32d7ebb7c6045ce950be567223b738f", "westus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    result = speech_recognizer.recognize_once()

    # Checks result.
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return ("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return ("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        return ("Speech Recognition canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        return ("Error details: {}".format(cancellation_details.error_details))
    print(result)
    print(result.text)
    '''


@app.route('/senti', methods=['POST'])
def reply():
    # with open('http://127.0.0.1:5000/chat', "r") as f:
    #    page = f.read()
    #tree = html.fromstring(page)

    message1 = request.get_json()
    message_json = json.dumps(message1)
    message_json1 = json.loads(message_json)
    message = message_json1['msg']
    try:
        a = TextBlob(message).sentiment.polarity
        b = TextBlob(message).sentiment.subjectivity

        if float(a) >= 0.3 and float(a) < 0.5 and float(b) >= 0.5:
            answer = "You seem to be in decent mood today. You wanna share some good news about you and your friend? "

            return jsonify(text=answer)

        if float(a) >= 0.3 and float(a) < 0.5 and float(b) < 0.5:
            answer = "Something seems to be in the good place. What is this? Tell me more. I am so curious"

            return jsonify(text=answer)

        elif float(a) >= 0.5 and float(b) >= 0.5:
            return jsonify(text='It is so good to see you being this happy. Even better than it sounds like something you feel strongly about')

        elif abs(float(a)) < 0.3 and abs(float(b)) < 0.5:
            list_of_greet = ['bye', 'goodbye', 'see you again', 'see you soon',
                             'goodnight', 'night', 'morning', 'good morning', "g'day mate"]
            funny_joke = ['The past, present and future walked into a bar. It was tense.', 'I hate people who use big words just to make themselves look perspicacious.', 'I thought my neighbours were lovely people. Then they went and put a password on their wi-fi.', 'A police recruit was asked during the exam, "What would you do if you had to arrest your own mother?" He said, "Call for backup.”', 'My boss told me yesterday, “You shouldnt dress for the job you have, dress for the job you want”. But when I turned up today in Ghostbusters clothes, he said I was fired.', 'Uh oh issa Trick day with no joke. Issa SAT WORDS OF THE DAY: Exhilarating. Definition: happy. Example: I am exhilarating about the SAT',
                          'Uh oh issa Trick day with no joke. It is SAT WORDS OF THE DAY: Galvanizing. Definition: happy. Example: I am galvanizing about the SAT',
                          'Uh oh issa Trick day with no joke. It is SAT WORDS OF THE DAY: Astounding. Definition: Amazing. Example: you are astounding']
            if message in list_of_greet:
                joke = random.choice(funny_joke)
                answer = 'Time for a little fun surprise: ' + joke
                return jsonify(text=answer)
            else:
                json1 = request.json
                text = json1['msg']
                mode_input = sentence_to_seq(text, vocabs_to_index)
                output = make_pred(sess, input_data, input_data_len, target_data_len,
                                   keep_prob, mode_input, batch_size, logits, index_to_vocabs)
                return jsonify(text=output)

        elif float(a) < -0.3 and float(a) > -0.5 and float(b) < 0.5:
            return jsonify(text='I detect a little irritation and resistance today. Are you or someone you know doing okay?')

        elif float(a) < -0.3 and float(a) > -0.5 and float(b) > 0.5:
            return jsonify(text='Oh no. You do not sound too good. When I am down, I like to listen to Mo Bamba. Lets listen to Mo Bamba together okay: https://www.youtube.com/watch?v=_1IL0cJwPSU')

        elif float(a) < -0.5 and float(b) > 0.5:
            answer = 'This is no joking matter. I care a lot about you so please trust me to help you. \nPlease look at the resources for the situation you are in: \nThreat and Abuse: http://www.childhelp.org/, \nLife Threatening Emergency: call 911, \nCyber Bully Helpline: https://dare.org \n I will always be here for you! '
            return jsonify(text=answer)

        else:
            answer = 'sorry but seems like I am getting tired. Maybe refresh me. Pleasee!'
            return jsonify(text=answer)
    except:
        return jsonify(text=message_json1['msg'])


if __name__ == '__main__':
    app.run(debug=True)
