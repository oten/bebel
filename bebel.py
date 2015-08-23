from flask import Flask, render_template, request, redirect, url_for
import json
import model

from pygments import highlight
from pygments.lexers import get_lexer_by_name, get_all_lexers
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
        ts = {v for k, v in data.items() if k.startswith('tag_')}
        data = {k: v for k, v in data.items() if not k.startswith('tag_')}
        data['tags'] = ts
        codes.add(**data)
        return redirect(url_for('bebel', idx=codes.next_idx - 1))
    
    elif idx == None:
        return render_template('bebel.html', lexers=lexers, tags=tags.search('root'))
    
    else:
        code = codes[str(idx)]
        lexer = get_lexer_by_name(code.language)
        html_code = highlight(code.code, lexer, HtmlFormatter())
        return render_template('bebel.html', html_code=html_code)


@app.route('/bebel/tag/new', methods=['GET', 'POST'])
def new_tag():
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
        return render_template('new_tag.html', tags=json.dumps(tags.as_dict()), root='"python e django"')
    

@app.route('/bebel/list')
@app.route('/bebel/list/<by_tag>')
def lst(by_tag=None):
    if by_tag:
        leaf_tags = tags.search(by_tag)
        idxs = set()
        for tag in leaf_tags:
            if tag in codes.codes_of_tag:
                idxs.update(codes.codes_of_tag[tag])

        lst = [codes[idx] for idx in idxs]
        return render_template('lst.html', codes=lst)
    else:
        return redirect(url_for('lst', by_tag='root'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
