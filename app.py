from flask import Flask, render_template, request  
from twilio.rest import Client
from pathlib import Path
from flask_recaptcha import ReCaptcha
from datetime import datetime

account_sid = 'redacted'
auth_token = 'redacted'
client = Client(account_sid, auth_token)
text = Path('/path/to/your/text').read_text()

app = Flask(__name__)           
app.config.update(dict(
    RECAPTCHA_ENABLED = True,
    RECAPTCHA_SITE_KEY = 'redacted',
    RECAPTCHA_SECRET_KEY = "6LeCS8YZAAAAAJ33nyml2GeX3siJruHrSp9cpqCS",
))
recaptcha = ReCaptcha()
recaptcha.init_app(app)
app.config['SECRET_KEY'] = 'redacted'

@app.route('/', methods=['GET'])                   
def hello():                      
        return render_template('covid.html')
        #return message.sid

@app.route('/', methods=['POST'])
def submit():
    if recaptcha.verify():
        ip = request.environ['REMOTE_ADDR']
        agent = request.headers.get('User-Agent')
        number = request.form.get('textbox')
        message = client.messages.create(body=text,from_='+redacted',to=number)
        f = open("twilio_log", "a")
        f.write(str(datetime.now()) + " " + ip + " " + agent + " " + number + " " + message.sid + "\n")
        f.close()
        return render_template('sent.html',number=number)
        pass
    else:
        #failed
        return render_template('failed.html')
        pass

@app.errorhandler(500)
def handle_exception(e):
    f = open("error_log", "a")
    f.write(str(datetime.now()) + " error" + "\n")
    f.close()
    return render_template('error.html')

if __name__ == "__main__":        
    app.run(host='0.0.0.0',ssl_context='adhoc')