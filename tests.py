import dat
import unittest
from components import Player
from components import Card

class Test_PlayerBank(unittest.TestCase):
    def test_purchase_valid(self):
        print("TEST PURCHASE VALID")
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
        print player.render()
        self.assertEqual(player.render(), resultstring)
    
    def test_reserve_valid(self):
        print("TEST RESERVE VALID")
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

    def test_taking_chips(self):
        print("TEST TAKING CHIPS")
        player3 = Player(dat)
        player3.name = "coderanger"
        player3.takes_chip('red')
        player3.takes_chip('blue')
        player3.takes_chip('green')
        resultstring = """
coderanger 

deck : ( bl-0 br-0      gr-0 wh-0 rd-0 )
chips: ( bl-1 br-0 go-0 gr-1 wh-0 rd-1 )
total: ( bl-1 br-0 go-0 gr-1 wh-0 rd-1 )
        """
        self.assertEqual(player3.render(), resultstring)


    def test_taking_4gold(self):
        print("TEST TAKING 4GOLD")
        card_seed = [
            {
            'uid'    : 72,
            'iden'   : 'blue',
            'points' : 0,
            'green'  : 2,
            'blue'   : 0,
            'white'  : 0,
            'red'    : 0,
            'brown'  : 2,
            },
            {
            'uid'    : 73,
            'iden'   : 'white',
            'points' : 0,
            'green'  : 2,
            'blue'   : 1,
            'white'  : 0,
            'red'    : 1,
            'brown'  : 1,
            },
            {
            'uid'    : 74,
            'iden'   : 'blue',
            'points' : 0,
            'green'  : 1,
            'blue'   : 0,
            'white'  : 1,
            'red'    : 1,
            'brown'  : 1,
            },
            {
            'uid'    : 75,
            'iden'   : 'brown',
            'points' : 1,
            'green'  : 0,
            'blue'   : 4,
            'white'  : 0,
            'red'    : 0,
            'brown'  : 0,
            }
        ]
        cards = [Card(**x) for x in card_seed]

        player4 = Player(dat)
        player4.name = "coderanger"
        for card in cards:
            player4.takes_card(card)
        resultstring = """
coderanger 

deck : ( bl-0 br-0      gr-0 wh-0 rd-0 )
chips: ( bl-0 br-0 go-3 gr-0 wh-0 rd-0 )
total: ( bl-0 br-0 go-3 gr-0 wh-0 rd-0 )
        """
        print(player4.render())
        self.assertEqual(player4.render(), resultstring)

    def test_buying_w_gold(self):
        card_seed = [
            {
            'uid'    : 72,
            'iden'   : 'blue',
            'points' : 0,
            'green'  : 2,
            'blue'   : 0,
            'white'  : 0,
            'red'    : 0,
            'brown'  : 2,
            },
            {
            'uid'    : 73,
            'iden'   : 'white',
            'points' : 0,
            'green'  : 2,
            'blue'   : 1,
            'white'  : 0,
            'red'    : 1,
            'brown'  : 1,
            },
            {
            'uid'    : 74,
            'iden'   : 'blue',
            'points' : 0,
            'green'  : 1,
            'blue'   : 0,
            'white'  : 1,
            'red'    : 1,
            'brown'  : 1,
            },
            {
            'uid'    : 75,
            'iden'   : 'brown',
            'points' : 1,
            'green'  : 0,
            'blue'   : 4,
            'white'  : 0,
            'red'    : 0,
            'brown'  : 0,
            }
        ]
        cards = [Card(**x) for x in card_seed]

        player5 = Player(dat)
        player5.name = "coderanger"
        # give him one blue chip so he can afford the last card
        player5.takes_chip('blue')
        for card in cards:
            print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
            print(player5.render())
            print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
            player5.takes_card(card)
        resultstring = """
coderanger 

deck : ( bl-0 br-1      gr-0 wh-0 rd-0 )
chips: ( bl-0 br-0 go-0 gr-0 wh-0 rd-0 )
total: ( bl-0 br-1 go-0 gr-0 wh-0 rd-0 )
        """
        print(player5.render())
        self.assertEqual(player5.render(), resultstring)

if __name__ == '__main__':
    unittest.main()  
    #main()