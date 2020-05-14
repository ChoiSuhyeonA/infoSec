import string
ENG_DICT =[]
file_input = open("dictionary.txt").read()
ENG_DICT = file_input.split("\n")
#print(len(ENG_DICT))
TempSTN = []
count =0
LETTERSwithWhiteSpace = string.ascii_letters + " "
STN = "This is an information security class 2019 @#$@#$@#"
for c in STN:
    if c in LETTERSwithWhiteSpace:
        if c is not '':
            TempSTN.append(c)
    #else:

STN =''.join(TempSTN)
#STN=STN[:-2]
print(STN)
STN = STN.upper().split(" ")
#print(STN)

matchNum = 0
for word in STN:
    if word in ENG_DICT:
        matchNum +=1
print("일치율: ",matchNum/len(STN)*100,"%")