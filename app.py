from flask import Flask, request, url_for
import datetime

app = Flask(__name__)


@app.route('/')
def hello_world():
    return f'Hello World!'


@app.route('/projects/')
@app.route('/projects/<float:val>')
def projectsFun(val=None):
    return f'Projects {val}'


@app.route('/about/', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        return "Post about"
    else:
        def link(endpointFun, displayName):
            return f"<a href={url_for(endpointFun.__name__)}>{displayName}</a>"
        return f'About, {link(projectsFun, "asdfsadfasdf")}'


print(hello_world())
if __name__ == '__main__':
    app.run()

s = "hey"

f"{s}"
