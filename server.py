from flask import Flask, request , jsonify
import RPi.GPIO as GPIO

# Mapping appliances/modules to words identifying them (in commands)
words = {"cfan" : {"fan", "ceiling"},
         "tube" : {"light", "tube", "tubelight"},
         "bulb" : {"bulb", "dim"}
        }

# Mapping appliances/modules to their ports 
# (220V Appliance --> Relay --> GPIO port) or (5V module/LED --> GPIO port)
GPIO_ports = {"tube":31,
              "cfan":33,
              "bulb":37}

GPIO.setmode(GPIO.BOARD)

def init_switches(inds):
    """Initializes the ports as GPIO output ports. Initially Off.
    inds    : list, Port numbers. 
    """
    for i in inds:
        GPIO.setup(i, GPIO.OUT, initial = 0)

def switch(ind,status):
    """Turns a port ON/True or OFF/False
    ind     : int, Port number
    status  : str, Turns port ON if status is 'on'. Else turns port OFF.
    """
    print("Switching :",ind,">>",status=='on')
    GPIO.output(ind, status=='on')

def trigger(command_string):
    """Uses token-matching to act on a command.
    command_string  : str, Command. For example : "fan off", "turn the light on", etc.
    status          : str (optional), Turns port ON if status is 'on'. Else turns port OFF.
    """
    # Convert command to lower case and split into words
    command_words = set(command_string.lower().split(" "))
    # Set status to 'on' if the word 'on' is present in the command (command_words)
    status = 'on' if 'on' in command_words else 'off'

    # Iterate over all appliances (ie. keys in words)
    for appliance in words:
        # If the command contains any words referring to the appliance
        if obj_words.intersection(words[appliance]):
            # Trigger the appliance to status
            port_num = GPIO_ports[appliance]
            switch(port_num,status)
            return

app = Flask(__name__)

@app.route('/prime', methods=['POST'])
def prime():
    """Endpoint to process incoming requests. 
    (POST requests with JSON mapping 'obj' to command)"""
    cont = request.get_json()
    if cont is not None:
        trigger(command_string=cont['obj'])
    return jsonify({"SUCCESS":True})

if __name__ == '__main__':  
    print('Starting Server')
    init_switches(GPIO_ports.values())	
    app.run(debug=True,
            use_reloader=False,
            host='0.0.0.0',
            port=8000
            ) #run app in debug mode on port 5000

