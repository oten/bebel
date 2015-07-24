from flask import Flask, render_template, request, redirect, url_for
from subprocess import call, Popen, PIPE
import json

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

app = Flask(__name__)

@app.route('/bebel/', methods=['GET', 'POST'])
@app.route('/bebel/<int:id>', methods=['GET', 'POST'])
def bebel(id=None):
    db = './db/escher.py'
    if request.method == 'POST':
        p = Popen([db, 'next_id'], stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        if err:
            output = '0'
        err = call([db, 'next_id', str(int(output) + 1)])
        err = call([db, str.strip(output), json.dumps(request.form)])
        print url_for('bebel')
        return redirect(url_for('bebel', id=int(output) ))
    
    elif id == None:
        return render_template('bebel.html', html_code='')
    
    else:
        p = Popen([db, '%d' % id], stdout=PIPE, stderr=PIPE)
        data, err = p.communicate()
        if not err:
            data = json.loads(data)
        else:
            data = {'code': '', 'language':'c'}
        return render_template('bebel.html',  
            html_code=highlight(data['code'], get_lexer_by_name(data['language']), HtmlFormatter()))

if __name__ == '__main__':
    app.run(debug=True)
