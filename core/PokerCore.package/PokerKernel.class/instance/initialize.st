initialize
initialize
	super.
	gameState := PreFlopState new.
	deck := nil.
	waitingList := Dictionary new.
	inGame := Dictionary new.
	sender := HttpSender new.
	players := Dictionary new.
	handFinished := true.