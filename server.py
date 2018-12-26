from flask import Flask, request , jsonify
import RPi.GPIO as GPIO
from json import loads
import traceback
import time
app = Flask(__name__)

GPIO.setmode(GPIO.BOARD)
words = {"cfan":{"fan","ceiling"},"tube":{"light","tube","tubelight"},"bulb":{"bulb","dim"}}
GPIo_inds = {"tube":31,"cfan":33,"bulb":37}

def init_switches(inds):
    for i in inds:
        GPIO.setup(i, GPIO.OUT, initial = 0)

def switch(ind,status):
    print(ind,status!='on')
    GPIO.output(ind, status!='on')

def trigger(obj_string,status='on'):
    obj_words = set(obj_string.lower().split(" "))
    status = 'on' if 'on' in obj_words else 'off'
    for key in words:
        if obj_words.intersection(words[key]):
            print("turn",key,status)          
            switch(GPIo_inds[key],status);return True

@app.route('/prime', methods=['POST'])
def prime():
    cont = request.get_json()
    if cont is not None:
        trigger(cont['obj'],'on')
    return jsonify({"SUCCESS":True})

if __name__ == '__main__':  
    print('Starting Server')
    init_switches(GPIo_inds.values())	
    app.run(debug=True,
            use_reloader=False,
            host='0.0.0.0',
            port=8000
            ) #run app in debug mode on port 5000

