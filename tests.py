import dat
import unittest
from components import Player
from components import Card

class Test_PlayerBank(unittest.TestCase):
    def test_purchase_valid(self):
        card_seed = {
            'uid'    : 18,
            'iden'   : 'green',
            'points' : 3,
            'green'  : 0,
            'blue'   : 2,
            'white'  : 2,
            'red'    : 2,
            'brown'  : 1,
            }
        card = Card(**card_seed)
        player = Player(dat)
        player.name = "coderanger"
        player.bank.add_chip(color='blue', quantity=3)
        player.bank.add_chip(color='white', quantity=2)
        player.bank.add_chip(color='red', quantity=2)
        player.bank.add_chip(color='brown', quantity=1)

        player.takes_card(card)
        resultstring = """
coderanger 

deck : ( bl-0 br-0      gr-1 wh-0 rd-0 )
chips: ( bl-1 br-0 go-0 gr-0 wh-0 rd-0 )
total: ( bl-1 br-0 go-0 gr-1 wh-0 rd-0 )
        """
        self.assertEqual(player.render(), resultstring)
    
    def test_reserve_valid(self):
        card_seed = {
            'uid'    : 18,
            'iden'   : 'green',
            'points' : 3,
            'green'  : 0,
            'blue'   : 2,
            'white'  : 2,
            'red'    : 2,
            'brown'  : 1,
            }
        card = Card(**card_seed)
        player2 = Player(dat)
        player2.name = "coderanger"
        player2.bank.add_chip(color='blue', quantity=1)
        player2.bank.add_chip(color='white', quantity=2)
        player2.bank.add_chip(color='red', quantity=1)
        player2.bank.add_chip(color='brown', quantity=1)

        player2.takes_card(card)
        resultstring = """
coderanger 

deck : ( bl-0 br-0      gr-0 wh-0 rd-0 )
chips: ( bl-1 br-1 go-1 gr-0 wh-2 rd-1 )
total: ( bl-1 br-1 go-1 gr-0 wh-2 rd-1 )
        """
        self.assertEqual(player2.render(), resultstring)


if __name__ == '__main__':
    unittest.main()  
    #main()