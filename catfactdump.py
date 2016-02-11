import requests,re,html, beautifulsoup

page= requests.get('http://user.xmission.com/~emailbox/trivia.htm').content.decode()

tags = re.findall('li>((.|\n|\r)*?)</li', page)
##for item in tags:
    ##print(' '.join(re.sub('<[^<]+?>', '',item[0]).split()))

with open('catdump.txt' , 'w') as dump:
    for item in tags:
        for item2 in item:
            print(beautifulsoup4(item2,convertEntities=beautifulsoup4.HTML_ENTITIES))
            dump.write(re.sub('<[^<]+?>', '',item2))
            dump.write('\n\n')
       

    
