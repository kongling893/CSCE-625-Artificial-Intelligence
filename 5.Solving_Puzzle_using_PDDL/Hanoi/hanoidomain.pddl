;;This is the domain of the Tower of Hanoi problem

(define (domain hanoidomain)
	(:requirements :strips)
	(:predicates (emptyupon ?x) (over ?x ?y) (smallerthan ?x ?y))
	(:action move
	 :parameters(?disk ?sourcepos ?targetpos)
	 :precondition( and (emptyupon ?disk) (emptyupon ?targetpos) (over ?disk ?sourcepos) (smallerthan ?disk ?targetpos))
	 :effect( and (not (emptyupon ?targetpos)) (not(over ?disk ?sourcepos)) (over ?disk ?targetpos) (emptyupon ?sourcepos)))
)
