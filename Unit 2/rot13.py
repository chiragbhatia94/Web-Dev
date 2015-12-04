import cgi
def rot13(x):
    news=""
    for i in x:
        if not i.isalpha():
            news+=i
        else:
            k=ord(i)+13
            if chr(k).isalpha():
                news+=chr(k)
            else:
                k-=26
                news+=chr(k)
    return cgi.escape(news,quote=True)

print rot13("Hello>")