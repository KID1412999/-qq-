#qq网络分析
import uin2uins
myuin={'yourqq':['qqnumber1','qqnumber2']}
s=[]
c=0
people=[]
def get_uin(main_uin):
	uin=[]
	uin2uins.friend.clear()
	for i in main_uin:
		t=uin2uins.uin2uins(i,'yourqq','password')
		t.remove(i)
		print(t,len(t))
	return t
def get_hisfuin(uin):
	global s,c
	hisf={}
	if c<=1:#遍历层数
		for i in [i for i in uin.values()]:
			for j in i:#j=18146...
				if j not in people:
					people.append(j)
					print(j,'--',c,end='-->')
					ls={j:get_uin([j])}#l={'18146':[...]}
					hisf.update(ls)
					print(ls)
					s.append(hisf)
					c+=1
					get_hisfuin(ls)
		return get_hisfuin(hisf)
get_hisfuin(myuin)
import networkx as nx
G=nx.Graph()
for i in s:
	for j,k	 in i.items():
		for l in k:
			G.add_edge(l,j)
print(s)
nx.draw(G , node_color='y' , with_labels=True,node_size=80)
import matplotlib.pyplot as plt
plt.show()
