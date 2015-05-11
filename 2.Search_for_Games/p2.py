#!/usr/bin/python
import Queue
from copy import deepcopy
class Node():
    def __init__(self,N = None,U = None, left = None, mid = None, right = None):
        self.N = N
        self.U = U
        self.left = left
        self.mid = mid
        self.right = right
	self.num = -1

    def __str__(self):
	q1 = Queue.Queue(-1)
	q2 = Queue.Queue(-1)
	q1.put(self)
	NodeStr = ""
        while not q1.empty() or not q2.empty():
		NodeStr = NodeStr+"\n"
		while not q1.empty():
			x = q1.get()	
			NodeStr = NodeStr+str(x.N)
			if x.left is not None: q2.put(x.left)
			if x.mid is not None: q2.put(x.mid)
			if x.right is not None: q2.put(x.right)
		NodeStr = NodeStr+"\n"
		while not q2.empty():
			x = q2.get()	
			NodeStr = NodeStr+str(x.N)
			if x.left is not None: q1.put(x.left)
			if x.mid is not None: q1.put(x.mid)
			if x.right is not None: q1.put(x.right)
        return NodeStr


class Tree():
   
    def __init__(self,N):
        if N<1: self.head = None
        elif N==1: self.head = Node(1)
        else: self.creatTree(N)           # self.head is used for MinMax tree
        self.head1 = deepcopy(self.head)  # self.head1 is used for alpha-belta pruning
        self.calculateUtilities(self.head,1)   #minmax algorithm
        self.alphabetaPruning(self.head1,1)      #alpha-beta pruning

    def __str__(self):
        return str(self.head)

    def creatTree(self,N):
        if N>3: 
                LeftNode = Tree(N-1).head
                MidNode = Tree(N-2).head
                RightNode = Tree(N-3).head
        if N==3: 
                LeftNode = Tree(N-1).head
                MidNode = Node(1)
                RightNode = None
        if N==2:
                LeftNode = Node(1)
                MidNode = None
                RightNode = None
        if N==1: 
                LeftNode = None
                MidNode = None
                RightNode = None
        self.head = Node(N,0,LeftNode,MidNode,RightNode)
        return   
    def calculateUtilities(self,Node,f):
        # f=1 means the player will do some action; otherwise the opposite will do some action
        # minmax algotithm used for generating utilities 
        if f==1: f_Next=0
        else: f_Next=1
        if Node is None:
                if f == 1: return 1
                else: return 0
        elif (Node.N==1):
                if f==1: Node.U = 0
                else: Node.U = 1
        else:
                U_left = self.calculateUtilities(Node.left,f_Next)
                U_mid = self.calculateUtilities(Node.mid,f_Next)
                U_right = self.calculateUtilities(Node.right,f_Next)
                if f==1:
                        Node.U = max(U_left,U_mid,U_right)  
                else:
                        Node.U = min(U_left,U_mid,U_right)  
        return Node.U

    def alphabetaPruning(self,Node,f):
        # alpha-beta pruning for generating uitilities
        if Node is None:
                if f == 1: return 1
                else: return 0
	elif (Node.N==1):
		if f == 1: return 0
                else: return 1
        
        if f==1:
                f_next = 0
                if (Node.left is not None) and (self.alphabetaPruning(Node.left,f_next)==1):
			Node.mid = None
			Node.right = None
                        return 1
                if (Node.mid is not None) and (self.alphabetaPruning(Node.mid,f_next)==1):
			Node.right = None
                        return 1
                if (Node.right is not None) and (self.alphabetaPruning(Node.right,f_next)==1):
                        return 1
		else: return 0
        if f==0: 
                f_next = 1
                if (Node.left is not None) and (self.alphabetaPruning(Node.left,f_next)==0):
			Node.mid = None
			Node.right = None
                        return 0
                if (Node.mid is not None) and (self.alphabetaPruning(Node.mid,f_next)==0):
			Node.right = None
                        return 0
                if (Node.right is not None) and (self.alphabetaPruning(Node.right,f_next)==0):
                        return 0
		else: return 1




def dot_gen_node(node):
	if node is None: return
	dot_gen_node.num += 1
	node.num = dot_gen_node.num
	print "\tN" + str(dot_gen_node.num) + "[label = \"" + str(node.N) + ":U=" + str(node.U) + "\"];"
	map(dot_gen_node, [node.left, node.mid, node.right])
	return 


def dot_gen_edge(node):
	if node is None: return
	i=0
	for n in [node.left, node.mid, node.right]:
		i=i+1
		if n is not None:
			print "\tN" + str(node.num) + " -> N" + str(n.num) + "[label=\""+str(i)+"\"];"
	map(dot_gen_edge, [node.left, node.mid, node.right])
	return


def dot_gen(node):
	print "digraph game_tree{"
	dot_gen_node(node)	
	dot_gen_edge(node)
	print "}"
	return

def dot_gen_Moore(N):
        GTree = Tree(N)
        head = GTree.head
        outPut = []
	f = 1
        while(head.left is not None):
		if f==1:
                	if(head.mid == None):                
                        	U_m = head.left.U
                	elif(head.right == None):                
                        	U_m = max(head.left.U,head.mid.U)
                	else: U_m = max(head.left.U,head.mid.U,head.right.U)
		else:
			if(head.mid == None):                
                        	U_m = head.left.U
                	elif(head.right == None):                
                        	U_m = min(head.left.U,head.mid.U)
                	else: U_m = min(head.left.U,head.mid.U,head.right.U)
		f=(f+1)%2 
                if head.left.U == U_m: 
                        outPut.append(1)
                elif head.mid.U == U_m: 
                        outPut.append(2)
                elif head.right.U == U_m: 
                        outPut.append(3)
                head=head.left
        outPut.append(0)   #Finnaly, the number of the remained matches is 0; no action in this state since we loose the game
        if N <=1: return
        print "digraph Moore{"
        for i in range(N):
                print "\tN"+str(N-i)+"[label = \""+str(N-i)+"-"+str(outPut[i])+"\"];"
                if (N-i)>3:
                        print "\tN"+str(N-i)+"->N"+str(N-i-1)+"[label=\"1\"];"
                        print "\tN"+str(N-i)+"->N"+str(N-i-2)+"[label=\"2\"];"
                        print "\tN"+str(N-i)+"->N"+str(N-i-3)+"[label=\"3\"];"
                if (N-i)==3:
                        print "\tN"+str(N-i)+"->N"+str(N-i-1)+"[label=\"1\"];"
                        print "\tN"+str(N-i)+"->N"+str(N-i-2)+"[label=\"2\"];"
                if (N-i)==2:
                        print "\tN"+str(N-i)+"->N"+str(N-i-1)+"[label=\"1\"];"
        print "}"
                        
                
                                 
        
        


# Under Ubuntu, you need to use   "python p2.py > out.dot "   to write the output
# into a dot file
N = 7                    # The initial number of the matches
dot_gen_node.num = 0
GTree = Tree(N)
dot_gen(GTree.head)      # generate the dot file for minmax algorithm
dot_gen_node.num = 0     
dot_gen(GTree.head1)     # generate the dot file for alpha-beta pruning
dot_gen_Moore(N)       #generate the dot file for moore machine



