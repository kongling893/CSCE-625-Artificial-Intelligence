(define (problem hanoiproblem)
(:domain starpuzzledomain)
(:objects  disk1 disk2 disk3  rod1 rod2 rod3 rod_o) 
(:init (emptyupon disk1) (emptyupon rod2) (emptyupon rod3) (emptyupon rod_o) (on_o rod_o)
	(smallerthan disk1 disk2)(smallerthan disk1 disk3)(smallerthan disk2 disk3)
	(disks disk1) (disks disk2) (disks disk3)
	(smallerthan disk1 rod1)(smallerthan disk1 rod2) (smallerthan disk1 rod3)(smallerthan disk1 rod_o)
	(smallerthan disk2 rod1)(smallerthan disk2 rod2) (smallerthan disk2 rod3)(smallerthan disk2 rod_o)
	(smallerthan disk3 rod1)(smallerthan disk3 rod2) (smallerthan disk3 rod3)(smallerthan disk3 rod_o)


	(over disk1 disk2)(over disk2 disk3) (over disk3 rod1))
(:goal 
	(and (over disk1 disk2)
	(over disk2 disk3) 
	(over disk3 rod3)))
)
