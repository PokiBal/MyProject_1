from flask import Flask
import sys

app =  Flask(__name__)
@app.route('/')

def hello_name():
   return f'Hello, {sys.argv[1]}'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
