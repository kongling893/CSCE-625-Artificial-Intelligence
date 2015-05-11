#!/usr/bin/python
import eqparser
import search
from copy import deepcopy
from math import *

#The definitions of actions

actions=[1,2,3,4,5,6,7,8,9,10,11]
#action = 1:exchange the left child node and the right child node
#action = 2:the left child node is "-", move its child node to the right side seu
#...
#action = 11:there is a ()

class Problem(object):
    def __init__(self, initial, goal=None):
        self.initial = initial
	self.goal = goal

    def actions(self, state): #definition of actions
        yield 1 
    	if(state.children[0].type == 'BINARYOP'):
    		if(state.children[0].leaf == '-'):
    			yield 2
		elif(state.children[0].leaf == '+'):
			yield 3
			yield 4
		elif(state.children[0].leaf == '/'):
			yield 5
		elif(state.children[0].leaf == '*'):
			yield 6
			yield 7
		elif(state.children[0].leaf == '^' and state.children[0].children[1].leaf == 2):
			yield 8
    	elif(state.children[0].type == 'UNARYOP'):
		if(state.children[0].leaf == '-'):
			yield 9
	elif(state.children[0].type == 'UNARYFUNCTION'):
		if(state.children[0].leaf == 'ln'):
			yield 10
		if(state.children[0].leaf == 'sqrt'):
			yield 11
		

    def result(self, state, action):
	if action == 1:
		temNode0 = deepcopy(state.children[1])
		temNode1 = deepcopy(state.children[0])
		Nstate = eqparser.Node('EQUALS',[temNode0,temNode1],'=')
        if action == 2:
		temNode0 = deepcopy(state.children[0].children[0])
		temNode1 = eqparser.Node('BINARYOP', [deepcopy(state.children[1]), deepcopy(state.children[0].children[1] )], '+')
		Nstate = eqparser.Node('EQUALS',[temNode0,temNode1],'=')
	if action == 3:
		temNode0 = deepcopy(state.children[0].children[0])
		temNode1 = eqparser.Node('BINARYOP', [deepcopy(state.children[1]), deepcopy(state.children[0].children[1] )], '-')
		Nstate = eqparser.Node('EQUALS',[temNode0,temNode1],'=')
	if action == 4:
		temNode0 = deepcopy(state.children[0].children[1])
		temNode1 = eqparser.Node('BINARYOP', [deepcopy(state.children[1]), deepcopy(state.children[0].children[0] )], '-')
		Nstate = eqparser.Node('EQUALS',[temNode0,temNode1],'=')
	if action == 5:
		temNode0 = deepcopy(state.children[0].children[0])
		temNode1 = eqparser.Node('BINARYOP', [deepcopy(state.children[1]), deepcopy(state.children[0].children[1] )], '*')
		Nstate = eqparser.Node('EQUALS',[temNode0,temNode1],'=')
	if action == 6:
		temNode0 = deepcopy(state.children[0].children[0])
		temNode1 = eqparser.Node('BINARYOP', [deepcopy(state.children[1]), deepcopy(state.children[0].children[1] )], '/')
		Nstate = eqparser.Node('EQUALS',[temNode0,temNode1],'=')
	if action == 7:
		temNode0 = deepcopy(state.children[0].children[1])
		temNode1 = eqparser.Node('BINARYOP',[deepcopy(state.children[1]), deepcopy(state.children[0].children[0] )], '/')
		Nstate = eqparser.Node('EQUALS',[temNode0,temNode1],'=')
	if action == 8:
		temNode0 = deepcopy(state.children[0].children[0])
		temNode1 = eqparser.Node('UNARYFUNCTION' , deepcopy(state.children[1]),'sqrt')
		Nstate = eqparser.Node('EQUALS',[temNode0,temNode1],'=')	
	if action == 9:
		temNode0 = deepcopy(state.children[0].children)
		temNode1 = eqparser.Node('UNARYOP', deepcopy(state.children[1]) ,'-')
		Nstate = eqparser.Node('EQUALS',[temNode0,temNode1],'=')
	if action == 10:
		temNode0 = deepcopy(state.children[0])
		temNode1 = eqparser.Node('BINARYOP', [eqparser.Node('SYMBOL', [], 'e'), deepcopy(state.children[1])], '^')
		Nstate = eqparser.Node('EQUALS',[temNode0,temNode1],'=')
	if action == 11:
		temNode0 = deepcopy(state.children[0].children)
		temNode1 = eqparser.Node('BINARYOP', [deepcopy(state.children[1]),eqparser.Node('INT',[], 2)],'^')
		Nstate = eqparser.Node('EQUALS',[temNode0,temNode1],'=')
	return Nstate
	

    def goal_test(self, state):
        if(state.type == 'EQUALS' and state.children[0].leaf == self.goal):
		return True
	else:
		return False

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self, state):
        return 0

#def optimizer(pro):
	
def dfs_distance_to_equal(p, goal, r):
	if(p.type == 'VARIABLENAME' and p.leaf == goal):
		return r 
	elif(p.type == 'BINARYOP' or p.type == 'EQUALS'):
		l = dfs_distance_to_equal(p.children[0], goal, r + 1) 
		r = dfs_distance_to_equal(p.children[1], goal, r + 1) 
		if(l != -1 and r != -1):
			return min(l, r)
		elif(l == -1 and r != -1):
			return r
		elif(l != -1 and r == -1):
			return l 
		else:
			return -1 ;
	elif(p.type == 'UNARYFUNCTION' or p.type == 'UNARYOP'):
		return dfs_distance_to_equal(p.children, goal, r+1) 
	else:
		return -1



class equaSimplifier():

	def __init__(self,p,var):
        	self.p = p
        
		self.error = -1
		self.var = var
		self.problem =Problem(self.p,var)
		self.result = search.astar_search(self.problem, lambda n: dfs_distance_to_equal(n.state, self.var, -1) ).state
		print "The result of the 1st step is:"+str(self.result)    
		self.result = self.simplifier(self.result)
        	self.outPut()
     
	def simplifier(self,Node): 
                if type(Node.children) != list: 
        	        if type(Node.children) == None: return Node
        	elif len(Node.children) == 0: return Node
		try:
        		if type(Node.children)!=list: 
                		var_in_Node = self.is_var_in(Node.children)
                		if var_in_Node:

                        		Node.children = self.simplifier(Node.children)
                		else:
                        		val1 = self.calculate(Node.children)
                			Node.children[0].leaf = str(eval(val1))
					Node.leaf = str(eval(Node.leaf+"("+val1+")"))
					Node.children = []
                		return Node
        		else:
				var_in_leftNode = self.is_var_in(Node.children[0])
                		if var_in_leftNode:
                        		Node.children[0] = self.simplifier(Node.children[0])
                		else:	
                        		val1 = self.calculate(Node.children[0])
					Node.children[0].leaf=str(eval(val1))
					Node.children[0].children = []

                		var_in_rightNode = self.is_var_in(Node.children[1])
                		if var_in_rightNode:
                        		Node.children[1] = self.simplifier(Node.children[1])
                		else:
                        		val2 = self.calculate(Node.children[1])
					val2 = val2.replace("^","**")
                                        Node.children[1].leaf=str(eval(val2))
					Node.children[1].children = []

				if not var_in_leftNode and not var_in_rightNode:
					Node.leaf = str(eval("("+val1+")"+Node.leaf+"("+val2+")"))
					Node.children = []

			if Node.leaf == "+":
                		if Node.children[0].leaf == "+":
                                	a = self.is_var_in(Node.children[1]) 
					b = self.is_var_in(Node.children[0].children[0])
					c = self.is_var_in(Node.children[0].children[1])
					if not a and not (b and c):
						ind = 1 if (b>c) else 0
						Node = eqparser.Node('BINARYOP',[eqparser.Node('BINARYOP',[Node.children[0].children[ind],Node.children[1]],'+'),deepcopy(Node.children[0].children[1 if 1-ind!=0 else 0])],'+')
						Node = self.simplifier(Node)
			if Node.leaf == "+":
                		if Node.children[1].leaf == "+":
					a = self.is_var_in(Node.children[0]) 
					b = self.is_var_in(Node.children[1].children[0])
					c = self.is_var_in(Node.children[1].children[1])
					if not a and not (b and c):
						ind = 1 if (b>c) else 0
						Node = eqparser.Node('BINARYOP',[eqparser.Node('BINARYOP',[Node.children[1].children[ind],Node.children[0]],'+'),deepcopy(Node.children[1].children[1 if 1-ind!=0 else 0])],'+')
						Node = self.simplifier(Node)
			if Node.leaf == "+":
                		if Node.children[1].leaf == "-":
					a = self.is_var_in(Node.children[0]) 
					b = self.is_var_in(Node.children[1].children[0])
					c = self.is_var_in(Node.children[1].children[1])
					if not a and not (b and c):
						if not b:
							Node = eqparser.Node('BINARYOP',[eqparser.Node('BINARYOP',[Node.children[0],Node.children[1].children[0]],'+'),deepcopy(Node.children[1].children[1])],'-')
						if not c:
							Node = eqparser.Node('BINARYOP',[eqparser.Node('BINARYOP',[Node.children[0],Node.children[1].children[1]],'-'),deepcopy(Node.children[1].children[0])],'+')
						Node = self.simplifier(Node)

			if Node.leaf == "+":
                		if Node.children[0].leaf == "-":
					a = self.is_var_in(Node.children[1]) 
					b = self.is_var_in(Node.children[0].children[0])
					c = self.is_var_in(Node.children[0].children[1])
					if not a and not (b and c):
						if not b:
							Node = eqparser.Node('BINARYOP',[eqparser.Node('BINARYOP',[Node.children[1],Node.children[0].children[0]],'+'),deepcopy(Node.children[0].children[1])],'-')
						if not c:
							Node = eqparser.Node('BINARYOP',[eqparser.Node('BINARYOP',[Node.children[1],Node.children[0].children[1]],'-'),deepcopy(Node.children[0].children[0])],'+')
						Node = self.simplifier(Node)	
			if Node.leaf == "-":
                		if Node.children[0].leaf == "+":
					a = self.is_var_in(Node.children[1]) 
					b = self.is_var_in(Node.children[0].children[0])
					c = self.is_var_in(Node.children[0].children[1])
					if not a and not (b and c):
						if not b:
							Node = eqparser.Node('BINARYOP',[eqparser.Node('BINARYOP',[Node.children[0].children[0],Node.children[1]],'-'),deepcopy(Node.children[0].children[1])],'+')
						if not c:
							Node = eqparser.Node('BINARYOP',[eqparser.Node('BINARYOP',[Node.children[0].children[1],Node.children[1]],'-'),deepcopy(Node.children[0].children[0])],'+')
						Node = self.simplifier(Node)
			if Node.leaf == "-":
                		if Node.children[1].leaf == "+":
					a = self.is_var_in(Node.children[0]) 
					b = self.is_var_in(Node.children[1].children[0])
					c = self.is_var_in(Node.children[1].children[1])
					if not a and not (b and c):
						if not b:
							Node = eqparser.Node('BINARYOP',[eqparser.Node('BINARYOP',[Node.children[0],Node.children[1].children[0]],'-'),deepcopy(Node.children[1].children[1])],'-')
						if not c:
							Node = eqparser.Node('BINARYOP',[eqparser.Node('BINARYOP',[Node.children[0],Node.children[1].children[1]],'-'),deepcopy(Node.children[1].children[0])],'-')
						Node = self.simplifier(Node)

			if Node.leaf == "-":
                		if Node.children[1].leaf == "-":
					a = self.is_var_in(Node.children[0]) 
					b = self.is_var_in(Node.children[1].children[0])
					c = self.is_var_in(Node.children[1].children[1])
					if not a and not (b and c):
						if not b:
							Node = eqparser.Node('BINARYOP',[eqparser.Node('BINARYOP',[Node.children[0],Node.children[1].children[0]],'-'),deepcopy(Node.children[1].children[1])],'+')
						if not c:
							Node = eqparser.Node('BINARYOP',[eqparser.Node('BINARYOP',[Node.children[0],Node.children[1].children[1]],'+'),deepcopy(Node.children[1].children[0])],'-')
						Node = self.simplifier(Node)
			if Node.leaf == "-":
                		if Node.children[0].leaf == "-":
					a = self.is_var_in(Node.children[1]) 
					b = self.is_var_in(Node.children[0].children[0])
					c = self.is_var_in(Node.children[0].children[1])
					if not a and not (b and c):
						if not b:
							Node = eqparser.Node('BINARYOP',[eqparser.Node('BINARYOP',[Node.children[0].children[0],Node.children[1]],'-'),deepcopy(Node.children[0].children[1])],'-')
						if not c:
							Node = eqparser.Node('BINARYOP',[deepcopy(Node.children[0].children[0]),eqparser.Node('BINARYOP',[Node.children[0].children[1],Node.children[1]],'+')],'-')
						Node = self.simplifier(Node)

			if Node.leaf == "/":
                		if Node.children[1].leaf == "/":
					a = self.is_var_in(Node.children[0]) 
					b = self.is_var_in(Node.children[1].children[0])
					c = self.is_var_in(Node.children[1].children[1])
					if not a and not (b and c):
						if not b:
							Node = eqparser.Node('BINARYOP',[eqparser.Node('BINARYOP',[Node.children[0],Node.children[1].children[0]],'/'),deepcopy(Node.children[1].children[1])],'*')
						if not c:
							Node = eqparser.Node('BINARYOP',[eqparser.Node('BINARYOP',[Node.children[0],Node.children[1].children[1]],'*'),deepcopy(Node.children[1].children[0])],'/')
						Node = self.simplifier(Node)
			if Node.leaf == "/":
                		if Node.children[0].leaf == "/":
					a = self.is_var_in(Node.children[1]) 
					b = self.is_var_in(Node.children[0].children[0])
					c = self.is_var_in(Node.children[0].children[1])
					if not a and not (b and c):
						if not b:
							Node = eqparser.Node('BINARYOP',[eqparser.Node('BINARYOP',[Node.children[0].children[0],Node.children[1]],'/'),deepcopy(Node.children[0].children[1])],'/')
						if not c:
							Node = eqparser.Node('BINARYOP',[deepcopy(Node.children[0].children[0]),eqparser.Node('BINARYOP',[Node.children[0].children[1],Node.children[1]],'*')],'/')
						Node = self.simplifier(Node)


			return Node
		except ZeroDivisionError:
			self.error = 0		

	def operation(self,Node):
        	x_in_leftNode = self.is_x_in(Node.children[0])
        	x_in_rightNode = self.is_x_in(Node.children[1])
        	if Node.leaf == "x":
                	return 0
        	else:
                	x=0

	def calculate(self,Node):	
                if type(Node.children) != list: 
        	        if type(Node.children) == None: return str(Node.leaf)
                        else:
				if Node.type == "UNARYOP" or Node.type == "UNARYFUNCTION":
                                	return str(Node.leaf)+"("+self.calculate(Node.children)+")"
                                return str(Node.leaf)+self.calculate(Node.children)
        	if len(Node.children) == 0 or Node.children == None: return str(Node.leaf)
        	if len(Node.children) == 1:
                        if Node.type == "UNARYOP" or Node.type == "UNARYFUNCTION":
                                return str(Node.leaf)+"("+self.calculate(Node.children)+")"
                        if len(Node.children.children) != 0: 
                                return str(Node.leaf)+"("+self.calculate(Node.children)+")"
                        return str(Node.leaf)+self.calculate(Node.children)
        	if len(Node.children) == 2:
			if Node.leaf == "=": return self.calculate(Node.children[0])+str(Node.leaf)+self.calculate(Node.children[1])
                        if len(Node.children[0].children)!= 0 and len(Node.children[1].children) !=0: 
                                return "("+self.calculate(Node.children[0])+")"+str(Node.leaf)+"("+self.calculate(Node.children[1])+")"
                        if len(Node.children[0].children) != 0:
                                return "("+self.calculate(Node.children[0])+")"+str(Node.leaf)+self.calculate(Node.children[1])
                        if len(Node.children[1].children) != 0:
                                return self.calculate(Node.children[0])+str(Node.leaf)+"("+self.calculate(Node.children[1])+")"
                        return self.calculate(Node.children[0])+str(Node.leaf)+self.calculate(Node.children[1])

	def diff_(self,Node):
		Node = self.simplifier(Node) 
		if Node == None or Node == []: return Node
		if Node.type == 'BINARYOP':
			var_in_leftNode = is_var_in(Node.children[0])
			var_in_rightNode = is_var_in(Node.children[1])
			if Node.leaf == "+" or Node.leaf == "-":
				if not var_in_leftNode: 
					Node.children[0].leaf ='0'
					Node.children[0].type = 'INT'
					Node.children[0].children = []
				if not var_in_rightNode: 
					Node.children[1].leaf ='0'
					Node.children[1].type = 'INT'
					Node.children[1].children = []
			if Node.leaf == "+" or Node.leaf == "-":
				if not var_in_leftNode:
					val1 = self.calculate( Node.children[0])
					Node.children[0].leaf = str(eval(val1))
					Node.children[0].type = 'FLOAT'
					Node.children[1] = self.diff_(Node.children[1])
				if not var_in_leftNode:
					val2 = self.calculate( Node.children[1])
					Node.children[1].leaf = str(eval(val2))
					Node.children[1].type = 'FLOAT'
					Node.children[0] = self.diff_(Node.children[0])
		return Node


	def is_var_in(self,Node):
                if Node.type == 'VARIABLENAME' or Node.leaf =="pi" or Node.leaf == "e":
                        return True
                else:
                        if type(Node.children) != list:
                                return self.is_var_in(Node.children)

                        elif not Node.children or len(Node.children)==0:
                                return False
                        else:
                                if len(Node.children)==1:
                                        return self.is_var_in(Node.children)
                                else:
                                        return self.is_var_in(Node.children[0]) or self.is_var_in(Node.children[1])
	def outPut(self):
	        if self.error == 0: 
		        print "x = undefined"
		        return
		print "The final result is:"+self.calculate(self.result)


while 1:
    try:
        s = raw_input('eq > ')   # use input() on Python 3
	var = raw_input('var > ')
    except EOFError:
        print
        break
    p = eqparser.parse(s)
    print "This is parsed at: " + repr(p)
    x = equaSimplifier(p,var)
    #print "This is parsed at: " + repr(p)
    #print "In infix form: " + str(p)
        

