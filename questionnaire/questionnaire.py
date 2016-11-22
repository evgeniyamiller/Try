from flask import Flask, render_template, request, url_for, redirect
import json

def readfile(name):
    f = open(name, 'r', encoding = 'utf-8')
    text = f.read()
    f.close()
    return text

def maketable(text):
    string = ''
    text = text.split('\n')
    for line in text:
        string += '<tr>'
        line = line.split('\t')
        for elem in line:
            string += '<td>' + elem +'</td>'
        string += '</tr>'
    return string

def writefile(name, text):
    f = open(name, 'w', encoding = 'utf-8')
    f.write(text)
    f.close()

def addition(name, d):
    l = []
    plus = ''
    for k in d:
        l.append(k)
        l = sorted(l)
        writefile('aa.txt', str(l))
    for i in l:
        plus = plus + d[i] + '\t'
    plus = plus[:-1]
    newtext = readfile(name) + '\n' + plus
    writefile(name, newtext)

def create_json(d):
     return json.dumps(d, ensure_ascii = False)
    
def newarray(text):
    arr = ['language', 'bite', 'come', 'die', 'drink', 'eat', 'fly', 'give', 'hear', 'kill', 'know', 'lie', 'say', 'see', 'sit', 'sleep', 'stand', 'swim', 'walk', 'comments']
    text = text.split('\n')
    newarr = []
    for line in text:
        d = {}
        line = line.split('\t')
        for elem in line:
            d[arr[line.index(elem)]] = elem
        newarr.append(d)
    return newarr[1:]

def search_word(word, lang, arr):
    string = ''
    for i in arr:
        if i['language'] == lang:
            if word in i:
                string = string + i[word] + '<br>'
    if string == '':
        string = 'no results'
    return string                  

app = Flask(__name__)

@app.route('/stats')
def stats():
    return render_template('stats.html', text = maketable(readfile('data.tsv')))

@app.route('/')
def form():
    if request.args:
        addition('data.tsv', request.args)
        return render_template('thanks.html')
    else:
        return render_template('form.html')
    
@app.route('/search')
def search():
    if request.args:
        lang = request.args['language']
        word = request.args['word']
        string = search_word(word, lang,(newarray(readfile('data.tsv'))))
        return render_template('results.html', language = lang, word = word, results = string)
    else:
        return render_template('search.html')

@app.route('/json')
def json_page():
    return render_template('json.html', text = create_json(newarray(readfile('data.tsv'))))

if __name__ == '__main__':
    #r = 'language\tbite\tcome\tdie\tdrink\teat\tfly\tgive\thear\tkill\tknow\tlie\tsay\tsee\tsit\tsleep\tstand\tswim\twalk\tcomments'
    #writefile('data.tsv', r)
    app.run(debug = True)
