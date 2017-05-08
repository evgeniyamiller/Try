import requests, json, re, matplotlib
import matplotlib.pyplot as plt
from datetime import date
import numpy as np

from matplotlib import rc 
matplotlib.rcdefaults() 

font = {'family': 'Courier New', 
'weight': 'normal'} 
rc('font', **font)

from matplotlib import style 
style.use('ggplot')

def api(method, parameters):
    req = 'https://api.vk.com/method/' + method + '?'
    for k in parameters:
        req += k + '=' + parameters[k] + '&'
    return json.loads(requests.get(req[:-1]).text)

def writefile(name, text):
    f = open(name, 'w', encoding='utf-8')
    f.write(text)
    f.close()
    
def get_comments(post_id, num_com, data):
    allcoms = ''
    averlencoms = []
    comments = api('wall.getComments', {'owner_id':'-91933860', 'post_id': str(post_id), 'count':'100'})
    if num_com > 100:
        comments['response'] += api('wall.getComments', {'owner_id':'-91933860', 'post_id': post_id, 'count':'100', 'offset':'100'})['response']
    for com in comments['response']:
        if type(com) == dict:
            text = com['text'].replace('<br>', '\n')
            allcoms += '* ' + cleaning(text) + '\n'
            if com['from_id'] > 0:
                city, age = get_info(com['from_id'])
                lencom = len(text.split())
                averlencoms.append(lencom)
                data.append([city, age, lencom])
    writefile(str(post_id) + ' comments.txt', allcoms)
    if len(averlencoms) != 0:
        average = sum(averlencoms)/len(averlencoms)
    else:
        average = 0
    return data, average     

def get_age(bdate):
    bdate = [int(i) for i in bdate.split('.')]
    if len(bdate) < 3:
        return 'unknown'
    today = date.today()
    age = today.year - bdate[2]
    if today.month < bdate[1]:
        age -= 1
    elif today.month == bdate[1] and today.day < bdate[0]:
        age -= 1
    return age

def get_info(author):
    info = api('users.get', {'user_ids':str(author), 'fields':'city,bdate'})
    if 'city' in info['response'][0]:    
        city = info['response'][0]['city']
        if city == '0' or city == 0:
            city = 'unknown'
    else:
        city = 'unknown'
    if 'bdate' in info['response'][0]:    
        age = get_age(info['response'][0]['bdate'])
    else:
        age = 'unknown'
    return city, age

def cleaning(text):
    import sys
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    res = re.search('\[id[0-9]*\|(.*?)\]', text) 
    if res:
        a, b = res.group(0), res.group(1)
        text = text.replace(res.group(0), res.group(1))
    return text.translate(non_bmp_map)

def newplot(x, y, cities, x_label, y_label, name):
    plt.figure(figsize=(20,10))
    plt.bar(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if name == 'city':
        plt.xticks(x, cities, rotation='vertical')
    plt.savefig(name +'.png', format='png', dpi=100)
    plt.clf()
    
def aver_lencoms(x, lencoms, t):
    d = {}
    b = []
    c = []
    for i in range(len(x)):
        a = x[i]
        if a != 'unknown':
            if a not in d:
                d[a] = [lencoms[i]]
            else:
                d[a].append(lencoms[i])
    for k in sorted(d.keys()):
        b.append(sum(d[k])/len(d[k]))
        if t == 'c':
            c.append(api('database.getCitiesById', {'city_ids':str(k)})['response'][0]['name'])
    if t == 'c':
        return c, b
    else:
        return  sorted(d.keys()), b
        
def main():
    posts = api('wall.get', {'owner_id':'-91933860', 'count':'100'})
    posts['response'] += (api('wall.get', {'owner_id':'-91933860', 'count':'100', 'offset':'100'})['response'])
    data, lenposts, averlencoms = [], [], []
    for post in posts['response']:
        if type(post) == dict:
            post_id = post['id']
            text = post['text'].replace('<br>', '\n')
            writefile(str(post_id) + '.txt', text)
            num_com = post['comments']['count']
            data, average = get_comments(post_id, num_com, data)
            lenposts.append(len(text.split()))
            averlencoms.append(average)
    lenposts, averlencoms = aver_lencoms(lenposts, averlencoms, 'l')
    newplot(lenposts, averlencoms, '', 'Длина поста', 'Средняя длина комментария', 'lenlen')
    ages, lencoms2 = aver_lencoms([i[1] for i in data], [i[2] for i in data], 'a')
    cities, lencoms3 = aver_lencoms([i[0] for i in data], [i[2] for i in data], 'c')
    newplot(ages, lencoms2, '', 'возраст', 'средняя длина комментария', 'age')
    newplot(range(len(cities)), lencoms3, cities, 'город', 'средняя длина комментария', 'city')
    
if __name__ == '__main__':
    main()
