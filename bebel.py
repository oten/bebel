from flask import Flask, render_template, request, redirect, url_for
import json
import model

from pygments import highlight
from pygments.lexers import get_lexer_by_name, get_all_lexers, ClassNotFound
from pygments.formatters import HtmlFormatter

app = Flask(__name__)
codes = model.Codes()
tags = model.Tags()

lexers = [lexer for lexer in get_all_lexers()]
lexers.sort(key=lambda x : x[0])


@app.route('/bebel/', methods=['GET', 'POST'])
@app.route('/bebel/<int:idx>', methods=['GET', 'POST'])
def bebel(idx=None):
    global codes, lexers, tags
    if request.method == 'POST':
        data = request.form.to_dict()
        data['tags'] = map(unicode.strip, data['tags'].split(',')[:-1])
        codes.add(**data)
        return redirect(url_for('bebel', idx=codes.next_idx - 1))
    
    elif idx == None:
        return render_template('bebel.html', lexers=lexers, tags=json.dumps(tags.as_dict()))
    
    else:
        code = codes[str(idx)]
        try:
            lexer = get_lexer_by_name(code.language)
        except ClassNotFound:
            lexer = get_lexer_by_name('Text')
        html_code = highlight(code.code, lexer, HtmlFormatter())
        return render_template('bebel.html', html_code=html_code, code=code)


@app.route('/bebel/tag/new', methods=['GET', 'POST'])
@app.route('/bebel/tag/new/<root>', methods=['GET', 'POST'])
def new_tag(root='root'):
    global tags
    if request.method == 'POST':
        data = request.form.to_dict()
        for k, v in data.items():
            if not v:
                continue
            lst = v.split(', ')
            tags[k] = tags[k] + lst if tags[k] else lst
            for i in lst:
                if not tags[i]:
                    tags[i] = list()
        return redirect(url_for('bebel'))
    else:
        return render_template('new_tag.html', tags=json.dumps(tags.as_dict()), root=root)
    

@app.route('/bebel/list')
@app.route('/bebel/list/<by_tag>')
def lst(by_tag=None):
    global codes, tags
    if by_tag:
        idxs = set()
        if by_tag in codes.codes_of_language:
            idxs.update(codes.codes_of_language[by_tag])
        for tag in tags.search(by_tag):
            if tag in codes.codes_of_tag:
                idxs.update(codes.codes_of_tag[tag])

        lst = [codes[idx] for idx in idxs]
        return render_template('lst.html', codes=lst)
    else:
        lst = [codes[str(i)] for i in range(codes.next_idx)]
        return render_template('lst.html', codes=lst)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
