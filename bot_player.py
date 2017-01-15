import random
import cards
from abstract_player import AbstractPlayer


class BotPlayer(AbstractPlayer):
    def __init__(self, name):
        AbstractPlayer.__init__(self, name)

    # ===========================================================================
    # #UPDATE:
    # ===========================================================================
    def update(self, gamestate):

        # =======================================================================
        # #GAMESTATE ANALYSIS
        # =======================================================================

        # IDENTIFY STAGE OF THE GAME
        stage = gamestate.get_stage()

        # IDENTIFY BLINDS:
        blinds = gamestate.getRoundBlinds()

        # IDENTIFY TOCALL:
        tocall = gamestate.get_player_bet_difference(self)

        print '%s :' % (self.getName())

        folded = False
        # fold in case you don't have enough money
        if tocall > self.getMoney():
            self.fold(gamestate)
            folded = True

        # =======================================================================
        # #POSSIBLE GAMESTAGES:
        # =======================================================================

        if not folded:
            # preflop:
            if stage == 'preflop':
                if tocall != 0:
                    self.call(gamestate)

            # flop
            elif stage == 'flop':
                if tocall == 0:
                    self.bet(gamestate, 2 * blinds)
                else:
                    self.call(gamestate)

            # turn
            elif stage == 'turn':

                if random.random() > 0.6:
                    if tocall == 0:
                        if gamestate.get_player_bets(self) == 0:
                            self.bet(gamestate, 2 * blinds)
                    else:
                        self.call(gamestate)
                else:
                    sumofknowncards = cards.listUnion(self.getHand(), gamestate.get_cards_on_table())

                    if len(cards.find_final_hands(sumofknowncards)) > len(sumofknowncards):
                        if gamestate.get_player_bets(self) == 0:
                            self.bet(gamestate, blinds + tocall)
                    else:
                        if random.random() < 0.2:
                            if tocall != 0:
                                self.fold(gamestate)
                        else:
                            self.call(gamestate)

            # river
            elif stage == 'river':
                if random.random() > 0.6:
                    if tocall == 0:
                        if gamestate.get_player_bets(self) == 0:
                            self.bet(gamestate, 2 * blinds)
                    else:
                        self.call(gamestate)
                else:
                    sumofknowncards = cards.listUnion(self.getHand(), gamestate.get_cards_on_table())

                    if len(cards.find_final_hands(sumofknowncards)) > len(sumofknowncards):
                        if gamestate.get_player_bets(self) == 0:
                            self.bet(gamestate, 2 * blinds + tocall)

                    else:
                        if random.random() < 0.2:
                            if tocall != 0:
                                self.fold(gamestate)
                        else:
                            self.call(gamestate)

        print
