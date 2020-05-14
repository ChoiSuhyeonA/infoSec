msg = 'hello world'

pad_r = len(msg)

if(pad_r%16 != 0):
    tmp = 16-pad_r
    for i in range(0,tmp):
        msg+= '0'

print(msg)