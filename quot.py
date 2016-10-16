from pyplasm import *

x = [.1,-.05,.01,-.05] 
p=x*5  #ripeto x 5 volte

a = QUOTE(p)

aa = PROD([a,a])

aaa = PROD([aa,a])

VIEW(a)
VIEW(aa)
VIEW(aaa)
