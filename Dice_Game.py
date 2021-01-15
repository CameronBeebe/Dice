import numpy as np
from collections import Counter

class Dice_Game:
    '''
    This simple multiplayer dice game is the Beebe family's variation of a popular dice game, we just call it "Dice".  
    
    Instructions:
    
    Players determine who goes first, and proceed taking turns in an order (typically clockwise around a table).
    
    Each player, in turn, proceeds by first shaking all six dice, 
    and proceeding along a decision tree of subsequent rolls.
    This tree ends in either a zero score, where a shake results in no dice count for points, 
    or the player "keeps" a number of dice which count for points.
    
    The point value of dice are determined per shake, 
    and point values do not change when mixed with dice kept from previous rolls.
    
    COUNTERS:
    
    One: 100
    Five: 50
    
    THREE-OF-A-KIND:
    Ones: 1000
    Sixes: 600
    Fives: 500
    Fours: 400
    Threes: 300
    Twos: 200
    
    STRAIGHT (1,2,3,4,5,6): 2500
    
    FLUSH (ALL-OF-A-KIND): Instant Win.
    
    On the occasion where all dice rolled are "counters", the dice must all be brought back and shook again.
    The turn proceeds as usual, adding the new shake points to the previous all-counter results.
    
    
    '''
    
    def __init__(self, players, num_dice=6):
        self.player_names = ['Player_{}'.format(name + 1) for name in [j for j in range(players)]]
        self.players = [self.Player(name=player) for player in self.player_names]
        self.dice = [self.Die(sides=6) for die in [i for i in range(num_dice)]]
        self.play_to = 7500
        self.winner = False
        self.turn = 0
        self.end_round = False
        self.score_to_beat = self.play_to
        
        
    def play_game(self):
        '''
        Loop over players to play a game, determining a winner with the highest score.
        '''
        
        print('PLAYING GAME')
        while self.end_round == False:
            
            for player in self.players:
                self.player_take_turn(player)


        for player in self.players:
            if player.went_out == 0:
                print('PLAYER', player.name, 'TRYING TO BEAT', self.score_to_beat)
                self.player_take_turn(player)
                
        scores = [player.score for player in self.players]
        print('SCORES AT END', scores)
        for player in self.players:
            if player.score == max(scores):
                print('THE WINNER IS:', player.name)
                player.winner = 1
                self.winner = True
                
        
    def object_list_to_faces(self,die_list):
        '''
        Function takes list (potentially including lists) of die objects and returns a list (of lists) of the die faces.
        '''

        face_list = [i.face_up if type(i) == Dice_Game.Die else [j.face_up for j in i] for i in die_list]

        return face_list
    
    def shake(self,dice_to_roll,Player):
        print('SHAKING')
        shook_dice = [die.roll() for die in dice_to_roll]
        #print('I,', Player.name, 'shook the dice:', [i.face_up for i in dice_to_roll])
        print('I,', Player.name, 'shook the dice:', self.object_list_to_faces(dice_to_roll))
        return dice_to_roll


        
    def player_take_turn(self,Player):
        
        '''
        Long method calling other methods for a player's turn.
        '''
        
        Player.turn += 1
        still_to_shake = self.dice.copy()
        #kept = []
        Player.turn_shakes = 0
        #print('length of self.dice', len(self.dice))
        
        while len(still_to_shake) > 0:
            if Player.turn_shakes == 0:
                print('lets goooo!')
                
                shake = self.shake(still_to_shake,Player)
                Player.turn_shakes += 1
                shake_faces = [i.face_up for i in shake]
                #print('shake:',shake_faces)
                counters, bring_back = self.detect_keepable(shake)
                kept, still_to_shake, nuthin = self.keep_dice(shake, counters)
                print('still to shake faces:', self.object_list_to_faces(still_to_shake))
                #kept.append(to_keep)
                Player.learning_history.extend(kept)
                print('KEPT:',self.object_list_to_faces(kept))
                score = self.kept_dice_faces_to_score(self.object_list_to_faces(kept))
                print('SCORE:', score)
                print('FIRST JUNCTION')
                print('On turn',Player.turn,'shake',Player.turn_shakes,', I,',Player.name,'kept', self.object_list_to_faces(kept),'and my total kept dice is', self.object_list_to_faces(kept))

                if bring_back:
                    print('bringing back from first junction.............')
                    still_to_shake = self.dice.copy()
                    
                stay = self.stay_or_go(score,Player)
                if stay:
                    Player.score += score
                    print('staying with score', score, ", Player's total score", Player.score)
                    break
                
            #elif kept != [] and Player.turn_shakes > 0:
            elif Player.turn_shakes >= 1:
                if nuthin == 0:
                    
                    print("keep 'em rollin'!")
                    print('kept so far:', self.object_list_to_faces(kept))

                    shake = self.shake(still_to_shake,Player)
                    Player.turn_shakes += 1
                    shake_faces = [i.face_up for i in shake]
                    print('shake:',shake_faces)
                    counters, bring_back = self.detect_keepable(shake)
                    to_keep, still_to_shake, nuthin = self.keep_dice(shake, counters)
                    #print('objects still to shake:',still_to_shake)
                    #print('still to shake faces:', [i.face_up for i in still_to_shake])
                    print('TO KEEP:', self.object_list_to_faces(to_keep))
                    kept.extend(to_keep)
                    Player.learning_history.append(kept)
                    score = self.kept_dice_faces_to_score(self.object_list_to_faces(kept))
                    print('SCORE:', score)
                    #print('KEPT:',kept)
                    print('SECOND JUNCTION')
                    print('On turn',Player.turn,'shake',Player.turn_shakes,', I,',Player.name,'kept', self.object_list_to_faces(to_keep),'and my total kept dice is', self.object_list_to_faces(kept))
                    
                    if bring_back:
                        print('bringing back from second junction.............')
                        still_to_shake = self.dice.copy()
                        
                    stay = self.stay_or_go(score,Player)
                    if stay:
                        Player.score += score
                        print('staying with score', score, ", Player's total score", Player.score)
                        break

            
                elif nuthin == 1:
                    print("you got nuthin:'",shake_faces, ". next player's turn.")
                    break
        
                print('OUTSIDE BREAK')
                if Player.score >= self.play_to:
                    Player.went_out = 1
                    if Player.score > self.score_to_beat:
                        self.score_to_beat = Player.score
                    self.end_round = True
                    print('PLAYER WENT OUT.  SCORE TO BEAT:', self.score_to_beat)
                    #Player.winner = True
        
        
        
    def detect_keepable(self, shook_dice):
        
        '''
        Method which sorts through the shook dice and returns a list (of lists) of potentially keepable dice.
        
        For example, if the dice objects shook show [1,2,5,4,4,4] detect_keepable will return: [[4,4,4],1,5]
        
        '''
        print('BEGIN DETECTING KEEPABLES')
        
        BRING_EM_BACK = 0
        
        #print('shook dice:', shook_dice)
        
        dice_faces = self.object_list_to_faces(shook_dice)
        #print('dice faces', dice_faces)
        #print('DOUBLE CHECK FACES:', [i.face_up for i in shook_dice])
        
        three_of_a_kinds = [i for i in Counter(dice_faces) if Counter(dice_faces)[i] >= 3]
        #print('three_of_a_kinds:', three_of_a_kinds)
        
        keepable_three_of_a_kinds = []
        for set_of_three in three_of_a_kinds:
            print('set_of_three',set_of_three)
            toak = []
            for i in shook_dice:
                if i.face_up == set_of_three and len(toak) <= 2:
                    toak.append(i)
            keepable_three_of_a_kinds.append(toak)
            #keepable_three_of_a_kinds.append([i for i in shook_dice if i.face_up == set_of_three])
            #print('appended keepable three of a kind objects:', keepable_three_of_a_kinds)

        keepable = keepable_three_of_a_kinds
        #print('keepable objects after adding three of a kinds:', keepable)
        print('keepable dice faces after adding three of a kinds:', self.object_list_to_faces(keepable))
        
        for i in shook_dice:
            if i.face_up == 1 or i.face_up == 5:
                keepable.append(i)
        #print('keepable objects after adding ones and fives:', keepable)
        print('keepable dice faces after adding ones and fives:', self.object_list_to_faces(keepable))     

        if set(dice_faces) == set([1,2,3,4,5,6]):
            keepable.append(shook_dice)
            #print('keepable objects after adding straight:', keepable)
            print('keepable dice faces after adding straight:', self.object_list_to_faces(keepable))
            
        print('total keepable list of dice faces:', self.object_list_to_faces(keepable))
        
        if all(die in keepable for die in shook_dice):
            print('total keepable list of dice faces:', self.object_list_to_faces(keepable))
            print('ALL COUNTERS.  BRING EM BACK!  NEED FUNCTION HERE!!!!')
            BRING_EM_BACK = 1
        
        return keepable, BRING_EM_BACK
    
    
    def keep_dice(self, shook_dice, keepable_list):
        '''
        Method for choosing which dice to keep.  
        
        This will in particular need to be interfaced for agent to learn.
        
        '''
        
        print('BEGIN KEEPING DICE')
        
        nuthin = 0
        
        #print('keepable object list:', keepable_list)
        #print('keepable dice faces list:', self.object_list_to_faces(keepable_list))
        #print('len keepable_list:', len(keepable_list))
        if len(keepable_list) is 0 or len(keepable_list) is 1:
            kept_dice = keepable_list
        else:
            #print('TESTING KEEPABLE LIST:', keepable_list)
            indexed_choice = np.random.choice(np.arange(len(keepable_list)))
            kept_dice = [keepable_list[indexed_choice]]
        #print('kept dice objects:', kept_dice)
        print('kept dice faces:', self.object_list_to_faces(kept_dice))

        for i in kept_dice:
            #print('object i in kept_dice:', i)
            if type(i) is list:
                print('i in kept_dice is list:', [j.face_up for j in i])
                for j in i:
                    #print('j object in list i:', j)
                    #print('j.face_up in list i:', j.face_up)
                    shook_dice.remove(j)
                    #print('shook_dice removed j object:',shook_dice)
                    print('remaining shook_dice faces after removing a', j.face_up, ':', [i.face_up for i in shook_dice])
            elif i in shook_dice:
                shook_dice.remove(i)

        dice_still_to_shake = shook_dice
        print('dice still to shake faces:', [i.face_up for i in dice_still_to_shake])
        
        if kept_dice == []:
            nuthin = 1

        return kept_dice, dice_still_to_shake, nuthin

    
    def kept_dice_faces_to_score(self,kept_dice_faces):
        
        '''
        Convert list of kept dice to a score.
        '''
        
        print('SCORING')

        score = 0

        if all(isinstance(i,int) for i in kept_dice_faces):
            if set(kept_dice_faces) == set([1,2,3,4,5,6]):
                score += 2500
                print('STRAIGHT', kept_dice_faces, 'SCORES:', score)
        else:
            for i in kept_dice_faces:
                if isinstance(i,list):
                    j = i[0]
                    if j >= 2:
                        score += j*100
                        print('TOAK', i, 'SCORES:', j*100)
                    else:
                        score += 1000
                        print('TOAK of ONES', i, 'SCORES:', 1000)
                else:
                    if i == 1:
                        score += 100
                        print('SINGLE', i, 'SCORES', 100)
                    elif i == 5:
                        score += 50
                        print('SINGLE', i, 'SCORES', 50)

        return score
    
    
    
    def stay_or_go(self,potential_score,Player):
        '''
        
        Function for agent to decide whether to stay with current dice, or keep shaking.
        
        FUTURE IMPLEMENTATION: Create player method(s) for more sophisticated decision-making.
        '''

        stay = 0
        
        if Player.score == 0:
            if potential_score >= 500:
                print("ON THE BOARD!!!!!!!!!!!!")
                stay = 1

        elif potential_score >= Player.threshold:
            stay = 1

        return stay
    
    
    class Die:
        '''
        Dice have a number of sides and, unless in motion, always have one face up.  

        Cocked dice are ignored, and motion/trajectories are assumed to be a random choice from the number of sides.
        '''

        def __init__(self,sides):
            self.sides = sides
            self.face_up = np.random.choice([i+1 for i in range(self.sides)])

        def roll(self):
            self.face_up = np.random.choice([i+1 for i in range(self.sides)])

            return self.face_up
    
    # Players as subclass, called in Dice_Game init
    class Player:
        '''
        Each player is equipped with several attributes, mainly for statistics and for future agent-based learning.
        '''
    
        def __init__(self,name):
            self.name = name
            self.turn = 0
            self.score = 0
            self.learning_history = []
            self.turn_shakes = 0
            self.game_shakes = 0
            self.threshold = self.det_threshold()
            self.went_out = 0
            self.winner = 0
            
            
        def det_threshold(self):
            '''
            Just a simple function to determine a random threshold so players are different. 
            
            In the future this should probably be dynamically changed as a function of game state and others.
            '''
            
            return (np.random.randint(10) + 1) * 50

            
