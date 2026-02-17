from flask import Flask, render_template, request, flash, redirect, url_for
from shared.totp import *
import qrcode
import os
import base64

app = Flask(__name__)
app.secret_key = os.urandom(16).hex()

timestep = 30
# RFC 6238 uses 8 in its example implementation, no explicit recommendations; Google defaults to 6 and that appears to be standard everywhere else
codelen = 6
secret_key = os.urandom(16)
qrstring = (f'otpauth://totp/CYBER_HMAC:TestServer?secret={base64.b32encode(secret_key).decode("utf-8")}&issuer=CYBER_HMAC')

img=qrcode.make(qrstring)
img.save('./server/static/qrcode.png')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/verifyCode', methods=['POST'])
def verify():

    codes = [generate_code(secret_key, timestep, codelen), generate_code(secret_key, timestep, codelen, offset=1)]
    print(codes)

    if request.method == "POST":
       testcode = request.form.get("code")
       print(testcode)
       if codes[0] == testcode or codes[1] == testcode:
           flash ("Code Verified", category="success")
       else:
           flash ("Bad Code", category='failure')
    else:
       flash("No code inputted", category='failure')
    return redirect('/2fa/')

if __name__ == '__main__':
    app.run(port = 5001)
