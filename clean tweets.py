FILE1 = "Scripts/hellasaltyrice"
FILE2 = "Scripts/export"

file = open(FILE1,'r')
file2 = open(FILE2,'w', encoding='utf-8')

for line in file:
    line = line.decode('utf-8')
    line = line[line.find("> ") + 2:-2]
    file2.write(line)
    file2.write("\n\n")
    
file.close()
file2.close()
