import dateparser
import dateparser.search as search

# test = "aaaa 2018/06/07"

# test =  "aaa 1/01/17-1021000575060"
# test = "2983"
# test = "2019"
# test = "2018"


# test = "aaa 2017/12/060"


# test = "2983 sads	aaa 1/01/17-1021000575060 sadsadd	2017-01-16 00:00:00	 sdadsada 2017-01-16 00:00:00"

# test = "3.06.2018​ created at 3.06.18​ with a cat 03.06.2018​ catly 12.06.2018​ withdraw d 06.24.2015 source.\n 12 may 2016​, october 11 2001 c​ at, 12 października 2011​, paid 28 sierpnia 2011 r.​ , doggy 28.08.2011​\n 28 VIII 2011​, lower than 28 sierpień 2011​ r., circus why and 28. sierpnia 2011 ​r. 28.VIII.2011​ rider s 9.11.12​\n may 5th​ xmay, koll saw 5th withdrawal 9/11/2018​ youth 3/04/2015​ mine 09/11/2017​\n qd 11 01 2000​. entries are due by January 4th, 2017​ at 8:00pm created 01/15/2005​ by ACME Inc. and associates.\n "

# test ="02.08.2017"
test = "2017-15-09"

# test = "17 maja 1965"
# test = "16 GRUDZIEŃ 1965"
# test = "16/GRUDZIEŃ/1965"
#
d = search.search_dates(test, languages=["pl"])
if d is not None:
    for i in range(len(d)):
        print(d[i][1])
#
# =====================================================
# fname = '/home/przemek/Pobrane/numery_faktur.csv'
# with open(fname) as f:
#     content = f.readlines()
# # you may also want to remove whitespace characters like `\n` at the end of each line
# content = [x.strip() for x in content]
#
# from random import randint
#
# used_ids = []
#
# random_conten = []
#
#
# for i in range(300):
#     while True:
#         rand = randint(0, len(content) - 1)
#         if rand not in used_ids:
#             used_ids.append(rand)
#             random_conten.append(content[rand])
#             break
#
# results = ""
# for l in random_conten:
#     d = search.search_dates(l, languages=["pl"])
#     results += l
#     if d is not None:
#         for i in range(len(d)):
#             results += ';'
#             results += str(d[i][1])
#     results+='\n'
#
# text_file = open("/home/przemek/Pobrane/result_not_line_by_line.csv", "w")
# text_file.write(results)
# text_file.close()

# ==================================================================

j = '/home/przemek/Desktop/pracai/dane/nazwyPlikówIOczekiwane.json'
with open(j) as f:
    nazwyPlikowIOczekiwane = f.read()

import json

js = json.loads(nazwyPlikowIOczekiwane)

nazwa_pliku = 'strona_z_internetu_3'
nazwa_pliku_z_format = nazwa_pliku + '.txt'

e = next(filter(lambda x: x['name'] == nazwa_pliku_z_format, js['files']), None)

print(e['expected'])

fname = '/home/przemek/Desktop/pracai/dane/' + nazwa_pliku_z_format
print("Odczytuje plik wejściowy")


def sprawdz(excpected, results):
    v = ''
    excpected.sort()
    results.sort()
    for e in excpected:
        cr = ''
        for r in results:
            if r == e:
                cr = r
                results.remove(r)
        v += e
        v += '   '
        v += cr
        v += '\n'
    if results: v += '----NIEZNALEZIONE------\n'
    for r in results:
        v += '             '
        v += r
        v += '\n'
    return v


with open(fname) as f:
    content = f.read()
    print("Odczytałem plik")

    results = ''
    print("Rozpoczynam szukanie dat")
    d = search.search_dates(content, languages=["pl"])
    print("Zakończyłem szukanie dat")
    same_daty = [e[1] for e in d]
    oczekiwane = e['expected']
    r = sprawdz(oczekiwane, same_daty)
    print(r)

    #
    #
    # print("Dodaje je do pliku")
    # results += "\n=============WYzNIKI=================\n"
    # if d is not None:
    #     for i in range(len(d)):
    #         results += ';'
    #         results += str(d[i][1])
    #         results += '\n  '
    # results += '\n'

    print(results)

