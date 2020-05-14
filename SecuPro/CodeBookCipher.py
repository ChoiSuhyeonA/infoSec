##모두 수작업

# decBook = {
#     "2": "H",
#     "3": "e",
#     "1": "l",
#     "4": "o",
#     "9": "w"
# }
##자동으로 decBook을 만드는 함수...
def makeCodeBook(encBook):
    decBook={}
    for k in encBook:
        #print(k)
        val = encBook[k]
        decBook[val] =k
    return decBook

##encryption...
##input : msg, encBook
##output : output
def encWithCodeBook(msg, encBook):

    for m in msg:
        if m in encBook:
            msg = msg.replace(m, encBook[m]) # 이러한 방식도 성립.
    return msg

#print(output)
##decryption....
## input : output, decBook
## output : plaintext
def decWithCodeBook(output, decBook):
    plaintext = ""
    for m in output:
        if m in decBook:
            plaintext += decBook[m]
        else:
            plaintext += m
    return plaintext

def decWithCodeBook2(output, decBook):

    for m in output:
        if m in decBook:
            output  = output.replace(m,decBook[m])
    return output
## main....
if __name__ == "__main__":
    encBook = {
        "H": "2",
        "e": "3",
        "l": "1",
        "o": "4",
        "W": "9",
        "r": "8",
        "d": "7"
    }
    msg = "Hello World"
    cipher = ""
    decBook = makeCodeBook(encBook)
    print(decBook)
    cipher = encWithCodeBook(msg,encBook)
    print("cipher:",cipher)
    plaintext = decWithCodeBook(cipher, decBook)
    print("plaintext:",plaintext)

