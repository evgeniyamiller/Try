from pymystem3 import Mystem
import random


def openfile(name):
    fIn = open(name, 'r', encoding = 'utf-8')
    lines = fIn.readlines()
    fIn.close()
    wordforms = []
    for line in lines:
        wordforms.append(line.split('\t')[1].strip('\n'))
    return wordforms


def ms(text):
    m = Mystem()
    ana = m.analyze(text)
    arr = []
    for word in ana:
        if 'analysis' in word:
            if len(word['analysis']) > 0:
                gr = word['analysis'][0]['gr']
                pos = gr.split('=')[0]
                gram = gr.split('=')[1].split('|')[0].strip('()')
                arr.append(word['text'].lower() + ' ' + pos + ',' + gr)
    return arr

def create_dict(arr):
    d = {}
    for el in arr:
        el = el.split()
        if el[1] in d:
            d[el[1]].append(el[0])
        else:
            d[el[1]] = [el[0]]
    return d
    
def main():
    corp_words = create_dict(ms(' '.join(openfile('1grams-3.txt'))))
    inp = ''
    print('Привет! Правила такие: ты вводишь фразу, а я отвечаю предложением, где все твои слова заменены на какие-то случайные другие слова той же части речи и с теми же грамматическими характеристиками. Чтобы закончить, введи "хватит". Поехали!')
    while inp != 'хватит':
        inp = input()
        words = ms(inp)
        string = []
        for word in words:
            string.append(random.choice(corp_words[word.split()[1]]))
        print(' '.join(string))

if __name__ == '__main__':
    main()
