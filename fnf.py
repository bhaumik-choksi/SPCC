import re

grammar = {}
First = {}
Follow = {}

def first(p):
	li = []
	l = grammar.get(p)

	for x in l:
		if x in ' ':
			continue
		elif x.islower():
			if x not in li:
				li.append(x)
		elif x.isupper():
			if len(x) == 1:
				if First.get(x) == None:
					first(x)
				li += First[x]
			else:
				for c in x:
					if First.get(c) == None:
						first(c)
					li += First[c]
					if 'ep' not in First[c]:
						break
		else:
			s = ''
			for c in x:
				print(c)
				if c.islower():
					print(c)
					s += c
				else:
					break
			if x not in li:
				li.append(x)
	First[p] = li

def follow(p):
	li = []
	if p in 'S':
		li.append('$')

	for keys,values in grammar.items():
		for x in values:
			if p in x:
				i = 0
				ind = x.index(p)
				if ind == len(x)-1:
					if Follow.get(keys) == None:
						follow(keys)
					li += Follow[keys]

				for i in range(ind+1,len(x)):
					if x[i].islower():
						print(x[i])
						li.append(x[i])
						break
					else:
						li += First[x[i]]
						if 'ep' not in First[x[i]]:
							print("asd")
							break
				if i == len(x):
					if Follow.get(keys) == None:
						follow(keys)
					li += Follow[keys]

	Follow[p] = li


#n = int(input("No of lines"))

file = open('program.txt','r')

for line in file:
	production = re.split('->|/|\n',line)
	p = production[0]
	l = []
	for i in range(1,len(production)):
		l.append(production[i])

	grammar[p] = l

for entry in grammar.keys():
	first(entry)

for entry in grammar.keys():
	follow(entry)

print(First)
print(Follow)