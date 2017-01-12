'''
pattern='ababab'
d=set(pattern)
print d
str="cc dd cc dd cc ee"
str1=str.split(" ")
str2={}
print str1
print map(pattern.find,pattern)
print map(str1.index,str1)
for key, value in zip(pattern, str1):
    print key, value
    if key not in pattern:
        if value not in str1:
            print 'saff'
    else:
        str2[key]=value
print str2
f= lambda x:map({}.setdefault,x,range(len(x)))
print f(pattern)
'''

a=[1,2,2,3,4,5,4,3,5,6]
b=set(a)
l=list(b)
print l, len(l)

