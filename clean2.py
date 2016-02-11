import ast

with open('Scripts/hellasaltyrice', encoding='utf-8') as f:
    with open('Scripts/export.txt','a',encoding='utf-8') as f2:
        for line in f:
            number, bytes_literal = line.split(' ',1)
            byte = ast.literal_eval(bytes_literal)
            text = byte.decode('utf-8')
            text = text[text.find("> ") + 2:]
            f2.write(text)
            f2.write('\n\n')
            
    

