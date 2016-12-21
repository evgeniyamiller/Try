import os, re

def openfile(name):
    fr = open(name, 'r', encoding = 'utf-8')
    f = fr.readlines()
    fr.close()
    return f
    
def create_code(f):
    d = {}
    s1 = ''
    s2 = ''
    analyse_id = 1
    for i in range(1, len(f)):
        if '{' in f[i]:
            wordform = f[i][:f[i].find('{')]
            lemma = f[i][f[i].find('{')+1:f[i].find('}')]
            punct_before = re.sub('_', '', re.sub('\n', '', f[i-1]))
            punct_after = re.sub('_', '', re.sub('\n', '', f[i+1]))
            if (wordform.lower(), lemma) not in d:
                d[(wordform.lower(), lemma)] = analyse_id
                s1 += 'insert into lemmas (wordform, lemma) values ("' + wordform.lower() + '", "' + lemma + '");' + '\n'
                analyse_id += 1
            s2 += 'insert into tokens (wordform, analyse_id, punct_before, punct_after) values ("' + wordform + '", "' + str(d[(wordform.lower(), lemma)]) + '", "' + punct_before + '", "' + punct_after + '");' + '\n'
    s = s1 + s2
    return s

def writefile(name, text):
    fw = open(name, 'w', encoding = 'utf-8')
    fw.write(text)
    fw.close()

def my_stem():
    s = r'C:\Users\evgen\Downloads\mystem.exe -n -c -d C:\Users\evgen\Desktop\text.txt C:\Users\evgen\Desktop\text1.txt'
    os.system(s)

def main():
    my_stem()
    writefile('sql.txt', create_code(openfile('text1.txt')))

if __name__ == '__main__':
    main()
