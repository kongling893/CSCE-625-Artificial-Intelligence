;;This is the domain of the star puzzle problem
(define (domain starpuzzledomain)
	(:requirements :strips)
	(:predicates (emptyupon ?x) (over ?x ?y) (smallerthan ?x ?y) (on_o ?x) (disks ?x) )

	(:action moveto_o
	 :parameters(?disk ?sourcepos ?targetpos)
	 :precondition( 
		and (emptyupon ?disk) 
		(emptyupon ?targetpos) 
		(over ?disk ?sourcepos) 
		(smallerthan ?disk ?targetpos) 
		(on_o ?targetpos) 
		(disks ?disk))
	 :effect( 
		and (not (emptyupon ?targetpos)) 
		(not(over ?disk ?sourcepos)) 
		(over ?disk ?targetpos) 
		(emptyupon ?sourcepos) 
		(on_o ?disk)))

	(:action movefrom_o
	 :parameters(?disk ?sourcepos ?targetpos)
	 :precondition( 
		and (emptyupon ?disk) 
		(emptyupon ?targetpos) 
		(over ?disk ?sourcepos) 
		(smallerthan ?disk ?targetpos) 
		(disks ?disk) 
		(on_o ?disk)
		(on_o ?sourcepos))
	 :effect( 
		and (not (emptyupon ?targetpos)) 
		(not(over ?disk ?sourcepos)) 
		(over ?disk ?targetpos) 
		(emptyupon ?sourcepos)
		 (on_o ?sourcepos) 
		(not(on_o ?disk))))
)
