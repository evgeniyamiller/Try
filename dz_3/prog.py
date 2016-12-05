import urllib.request, re

def search(text, regex):
    res = re.search(regex, text)
    if res != None:
        return res.group(1)
    else:
        return

def get_code(adds):
    page = urllib.request.urlopen(adds)
    text = page.read().decode('utf-8')
    return text
    
def get_text(text):
    if 'Все новости спорта читайте на' in text:
        text = text.split('Все новости спорта читайте на')[0]
    elif 'Подписывайтесь на наш канал' in text:
        text = text.split('Подписывайтесь на наш канал')[0]
    text = re.sub('<p class="item-title">.*?</p>', '', text)
    newtext = ''
    newtext += search(text, '<h1 .*?([А-Я].*?)</') + '\n'
    result = re.findall('<p.*?([А-Я].*?)<', text)
    for el in result:
        newtext += el + ' '
    newtext = textwork(newtext)
    return create_set(newtext)

def create_set(text):
    text = text.split()
    a = []
    for el in text:
        a.append(el.lower())
    return set(a)
    
def textwork(text):
    text = re.sub('[\.,:;/?///\/(/)—"…]', ' ', text)
    text = text.replace('Уважаемые пользователи  Просим отнестись с пониманием и добавить сервис в список исключений вашей программы для блокировки рекламы  AdBlock и другие  ', '')
    text = text.replace('&nbsp', ' ')
    text = text.replace('&mdash', ' ')
    text = text.replace('&quot', ' ')
    return(text)

def writefile(name, text):
    fw = open(name, 'w', encoding = 'utf-8')
    fw.write(text) 
    fw.close()    

def intersection(sets):
    newset = sets[0] & sets[1] & sets[2] & sets[3]
    newset = sorted(list(newset))
    writefile('intersection.txt', '\n'.join(newset))

def difference(sets):
    newset = (sets[0] | sets[1] | sets[2] | sets[3]) - (sets[0] & sets[1]) - (sets[0] & sets[2]) - (sets[2] & sets[1]) - (sets[0] & sets[3]) - (sets[1] & sets[3]) - (sets[2] & sets[3])
    newset = sorted(list(newset))
    writefile('difference.txt', '\n'.join(newset))

def main():
    sets = []
    arr = ['http://www.liveresult.ru/news/%D0%A8%D0%B0%D1%85%D0%BC%D0%B0%D1%82%D1%8B/c_19624/', 'https://ria.ru/sport/20161201/1482628456.html', 'http://izvestia.ru/news/648816', 'http://tass.ru/sport/3829784']
    for adds in arr:
        sets.append(get_text(get_code(adds)))
    intersection(sets)
    difference(sets)

if __name__ == '__main__':
    main()
