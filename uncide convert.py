


with open('tweets.txt', encoding = 'utf-8') as f:
    with open('tweets2.txt', 'w', encoding = 'utf-8') as f2:
        for line in f:
            text = line.decode('utf-8')
            f2.write(text)
            
