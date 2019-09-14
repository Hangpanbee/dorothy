from flask import Flask, render_template
import azure.cognitiveservices.speech as speechsdk

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat')
def chat():
    return render_template('Chatbot.html')

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


if __name__ == '__main__':
    app.run(debug=True)