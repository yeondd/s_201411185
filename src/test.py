
word = ['sangmyung university', 'university']

d = dict()
for e in word:
    for w in e.split(): 
        if w not in d:
            d[w]=1
        else:
            d[w]=d[w]+1
print "key-key value",d 
print "stored charaters number(without overwirte): ", len(d)
print "key: ",d.keys()
print "value:", d.values()