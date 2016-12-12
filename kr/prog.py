import json, re
from flask import Flask, render_template, request, url_for, redirect

d = {}

def openfile(name):
    file = open(name, 'r', encoding = 'utf-8')
    text = file.readlines()
    file.close()
    return text

def makedict(text, d):
    for line in text:
        if 'lex:' in line:
            word = line[6:].replace('\n','')
        elif 'gramm:' in line:
            d[word] = []
            d[word].append(line[8:].replace('\n',''))
        elif 'trans_ru:' in line:
            d[word].append(line[11:].replace('\n',''))
    return d

def rus_udm(d):
    rd = {}
    for k in d:
        d[k][1] = re.sub('[0-9]\.', ',', d[k][1])
        for i in d[k][1].split(','):
            if i.startswith(' '):
                i = i[1:]
            if i.endswith(' '):
                i = i[:-1]
            if i != '':
                if i not in rd:
                    rd[i] = [[k, d[k][0]]]
                else:
                    rd[i].append([k, d[k][0]])
    return rd

def writefile(name, text):
    fw = open(name, 'w', encoding = 'utf-8')
    fw.write(text) 
    fw.close()

def main():
    global d
    for i in ['udm_lexemes_ADJ.txt', 'udm_lexemes_IMIT.txt']:
        d.update(makedict(openfile(i), d))
    writefile('json.json', json.dumps(d, ensure_ascii=False))
    writefile('jsonrus.json', json.dumps(rus_udm(d), ensure_ascii=False))

app = Flask(__name__)

@app.route('/')
def search():
    global d
    if request.args:
        word = request.args['word']
        string = d[word][1]
        return render_template('results.html', word = word, string = string)
    else:
        return render_template('search.html')

if __name__ == '__main__':
    main()
    app.run(debug = True)
