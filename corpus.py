import urllib.request, os, re

def search(text, regex):
    res = re.search(regex, text)
    if res != None:
        return res.group(1)

def createmeta(text, pageUrl):
    author = search(text, 'Автор: (.*?)\t\t\t\t</span>')
    header = search(text, '<title>(.*?)  </title>')
    header = header.replace('&quot;', '"')
    created = search(text, 'Обновлено (.*?)		</span>')
    topic = search(text, 'Категория: <a href=".*?">(.*?)</a>')
    publ_year = str(created)[-4:]
    month = str(created)[3:5]
    meta = {'author':author, 'month':month, 'header':header, 'created':created, 'topic':topic, 'pageUrl':pageUrl, 'publ_year':publ_year}
    return meta

def textwork(text):
    res = re.findall('\n(.*?)</p>', text)
    newtext = '\n'.join(res)
    newtext = newtext.replace('&nbsp;', '')
    newtext = newtext.replace('<br />', '\n')
    newtext = newtext.replace('Вам необходимо зарегистрироваться на сайте.', '')
    newtext = newtext.replace('© Рославльская правда 2012.\n Использование материалов сайта в сети Интернет, в печатных СМИ, на радио и телевидении  только с разрешения редакции. \n При публикации материалов, ссылка на сайт обязательна. \n Мнение редакции не всегда совпадает с мнением авторов публикаций.\n За высказывания посетителей сайта редакция ответственности не несет.', '')
    newtext = re.sub('<.*?>', '', newtext)
    newtext = re.sub('var.*?;', '', newtext)
    return newtext

def writefile(name, text):
    fw = open(name, 'w', encoding = 'utf-8')
    fw.write(text) 
    fw.close()    

def download_page(pageUrl):
    try:
        page = urllib.request.urlopen(pageUrl)
        text = page.read().decode('utf-8')
        return text
    except:
        print('Error at', pageUrl)
        return

def createdirs(year, month, f):
    os.chdir(os.getcwd() + '\\' + f)
    if not os.path.exists(year):
        os.makedirs(year)
    os.chdir(os.getcwd() + '\\' + year)
    if not os.path.exists(month):
        os.makedirs(month)
    os.chdir(os.getcwd() + '\\' + month)
    

def newplain(text, meta):
    createdirs(meta['publ_year'], meta['month'], 'plain')
    name = str(meta['i']) + '.txt'
    alltext = '@au ' + str(meta['author']) + '\n@ti ' + str(meta['header']) + '\n@da ' + str(meta['created']) + '\n@topic ' + str(meta['topic']) + '\n@url ' + str(meta['pageUrl']) + '\n' + text
    writefile(name, alltext)
    newdir = str(os.getcwd())[:-13]
    os.chdir(newdir)

def plain(text, meta):
    createdirs(meta['publ_year'], meta['month'], 'plain')
    name = str(meta['i']) + '.txt'
    writefile(name, text)
    newdir = str(os.getcwd())[:-13]
    os.chdir(newdir)

def mystem_xml(text, meta):
    createdirs(meta['publ_year'], meta['month'], 'mystem-xml')
    newname = str(meta['i']) + '.xml'
    writefile(newname, text)
    newdir = str(os.getcwd())[:-18]
    os.chdir(newdir)

def mystem_plain(text, meta):
    createdirs(meta['publ_year'], meta['month'], 'mystem-plain')
    name = str(meta['i']) + '.txt'
    row = r'C:\Users\evgen\Downloads\mystem.exe -n -d -i C:\Users\evgen\Desktop\Roslavlskajapravda\plain\%s\%s\%s C:\Users\evgen\Desktop\Roslavlskajapravda\mystem-plain\%s\%s\%s'
    os.system(row % (meta['publ_year'], meta['month'], name, meta['publ_year'], meta['month'], name))
    fr = open(name, 'r', encoding = 'utf-8')
    f = fr.read() 
    fr.close()
    newdir = str(os.getcwd())[:-20]
    os.chdir(newdir)
    return f

def metatable(meta):
    row = '%s\t%s\t\t\t%s\t%s\tпублицистика\t\t\t%s\t\tнейтральный\tн-возраст\tн-уровень\tрайонная\t%s\tРославльская правда\t\t%s\tгазета\tРоссия\tСмоленская область\tru' 
    newrow = row % (meta['path'], meta['author'], meta['header'], meta['created'], meta['topic'], meta['pageUrl'], meta['publ_year'])
    fr = open('metadata.tsv', 'r')
    f = fr.read()
    fr.close()
    f = f + '\n' + newrow
    fw = open('metadata.tsv', 'w') 
    fw.write(f) 
    fw.close()

def createfiles(text, pageUrl, i):
    meta = createmeta(text, pageUrl)
    meta['i'] = i
    meta['path'] = str(os.getcwd()) + '\\' + meta['publ_year'] + '\\' + meta['month'] + '\\' + str(i) + '.txt'
    metatable(meta)
    newtext = textwork(text)
    plain(newtext, meta)
    mystem_xml(mystem_plain(newtext, meta), meta)
    newplain(newtext, meta)

def main():
    commonUrl = 'http://ropravda.ru/index.php/'
    os.makedirs('plain')
    os.makedirs('mystem-xml')
    os.makedirs('mystem-plain')
    writefile('metadata.tsv', 'path\tauthor\tsex\tbirthday\theader\tcreated\tsphere\tgenre_fi\ttype\ttopic\tchronotop\tstyle\taudience_age\taudience_level\taudience_size\tsource\tpublication\tpublisher\tpubl_year\tmedium\tcountry\tregion\tlanguage') 
    for i in range(11,2280):
        pageUrl = commonUrl + str(i)
        text = download_page(pageUrl)
        if text != None:
            createfiles(text, pageUrl, i)

if __name__ == '__main__':
    main()


