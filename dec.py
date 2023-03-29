from flask import Flask, render_template, request
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/result', methods=['POST'])
def result():
    text = request.form['text']
    key = request.form['key']
    mode = request.form['mode']
    
    if mode == 'e':
        result = encode(key, text)
    elif mode == 'd':
        result = decode(key, text)
    else:
        result = 'Invalid mode'
    
    return render_template('result.html', result=result)

def encode(key, message):
    enc = []
    for i in range(len(message)):
        key_c = key[i % len(key)]
        enc.append(chr((ord(message[i]) + ord(key_c)) % 256))
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, message):
    dec = []
    message = base64.urlsafe_b64decode(message).decode()
    for i in range(len(message)):
        key_c = key[i % len(key)]
        dec.append(chr((256 + ord(message[i]) - ord(key_c)) % 256))
    return "".join(dec)

if __name__ == '__main__':
    app.run(debug=True)
