#
my_file = open("s.txt")
s = my_file.read()
my_file.close()

s = s.replace(' ', '')

x = 0
for i in s:
    
    if i == '(':
        print(i, end='')
        print('\n', end='')
        x +=1
        print('    '*x, end='')
    elif i == ')':
        print('\n', end='')
        x -=1
        print('    '*x, end='')
        print(i, end='')
    elif i == ',':
        print(i, end='')
        print('\n', end='')
        
        print('    '*x, end='')
    else:
        print(i, end='')
        
        
