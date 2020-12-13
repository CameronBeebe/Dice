Creating a simple class for die in order to simulate a simple dice game.

TO DO:

1.  Add players. MOSTLY DONE

2.  Add Player scores and keep track of them 

3.  Add rules (ones, fives, 3-of-a-kind, 1-2-3-4-5-6, 6-of-a-kind, etc.)

4.  Add mechanics for keeping dice and continuing to roll remaining.  STARTED, but while loop needs to be properly debugged.  

I think this may be functional.

5.  Create function converting kept dice to score (with intermittent steps to keep track of e.g. three of a kinds), needed for 2

6.  Need to overhaul and debug detect_keepable and keep_dice since they were poorly sketched and omitted reference to die objects in original code.  FIXED I THINK

7.  Need to implement option to hold without continuing to roll.  Then pass held dice into function in 5.

8.  Create verbosity logic. Maybe verbose = 0, 1, or 2, where 1 shows faces and 2 shows faces and die objects in memory.

9.  Make player_take_turn while loop logic more elegant...

7.  Compactify all lengthy list comprehensions?  Maybe use type()==Dice_Game.Die?