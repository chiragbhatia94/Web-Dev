import cgi
def shift_n_letters(letter, n):
    n%=26
    c=ord(letter)
    c=c+n
    if c>ord('z'):
        e=c-ord('z')
        c=ord('a')+e-1
    elif c<ord('a'):
        e=ord('a')-c
        c=ord('z')-e
    return chr(c)

def rot13(x):
    news=""
    for i in x:
        if not i.isalpha():
            news+=i
        else:
            if i.islower():
                news+=shift_n_letters(i,13)
            else:
                news+=shift_n_letters(i.lower(),13).upper()
    return cgi.escape(news,quote=True)

print rot13("Hello, everyone! What are your names?")
print rot13("Uryyb, rirelbar! dung ner lbhe anzrf?")

print rot13("U")
print rot13("W")