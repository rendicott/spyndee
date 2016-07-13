from jinja2 import Template
import random
import components
import dat

# jinja2 template for making a basic text board for debugging and development visualization
jtpl_board = """
{% for noble in nobles %}
NOBLE----{{ noble }}{% endfor %}


                   {{stack_large}} | {{card_large_1}} | {{card_large_2 }} | {{card_large_3 }} | {{card_large_4}}
{{chips_red}}

{{chips_white}}              {{stack_medium}} | {{card_medium_1}} | {{card_medium_2 }} | {{card_medium_3 }} | {{card_medium_4}}

{{chips_blue}}
                   {{stack_small}} | {{card_small_1}} | {{card_small_2 }} | {{card_small_3 }} | {{card_small_4}}
{{chips_brown}}

{{chips_green}}

{{chips_gold}}

{{ player_1 }} {{player_2 }} {{player_3}} {{player_4}}

"""

class Board():
    """ The main class for building and interacting with the game board.

    The init method of this class will start the process of loading data
    and initializing all the other components. 
    """
    def __init__(self,players,data):
        self.tpl = Template(jtpl_board)
        self.players = players
        self.points_to_win = data.points_to_win
        self.max_tokens_in_hand = data.max_tokens_in_hand
        self.max_reserve_cards = data.max_reserve_cards
        # instantiate the properties for chip counts
        self.mode_chips_red = 7
        self.mode_chips_blue = 7
        self.mode_chips_green = 7
        self.mode_chips_brown = 7
        self.mode_chips_white = 7
        self.mode_chips_gold = 5
        self.mode_nobles = 5
        # set actual chip counts based on game mode (i.e., num of players)
        self.mode_set(data)
        # nwo build the chip stacks
        self.stack_chips_red = components.Chips('red','rd',self.mode_chips_red)
        self.stack_chips_white = components.Chips('white','wh',self.mode_chips_white)
        self.stack_chips_green = components.Chips('green','gr',self.mode_chips_green)
        self.stack_chips_brown = components.Chips('brown','br',self.mode_chips_brown)
        self.stack_chips_gold = components.Chips('gold','go',self.mode_chips_gold)
        self.stack_chips_blue = components.Chips('blue','bl',self.mode_chips_blue)
        # instantiate nobles inventory from data
        self.nobles = components.Nobles(self.mode_nobles)
        self.nobles.load_nobles(data.nobles)
        self.nobles.shuffle_build_active(self.mode_nobles)
        # instantiate cards inventory from data 
        self.cards_inventory = components.Cards()
        self.cards_inventory.load_cards(data.cards)
        self.cards_small_active = components.Cards()
        self.cards_medium_active = components.Cards()
        self.cards_large_active = components.Cards()
        self.cards_classify_sizes()
        self.cards_active = [self.cards_small_active,self.cards_medium_active,self.cards_large_active]
        self.shuffle_all(self.cards_active)

        self.base_board = self.initialize_base_board()

    def render(self):
        """ Method for rendering the board. For now just text. 
        """
        return self.tpl.render(**self.base_board)
    def mode_set(self,data):
        """ Method for selecting chip counts and noble counts
        based on desired players and static data from the dat file.
        """
        m = 0

        for mode in data.modes:
            if self.players == data.modes.get(mode).get('players'):
                m = mode
            if self.players == 4:
                m = 1
        self.mode_chips_red = data.modes.get(m).get('red')
        self.mode_chips_blue = data.modes.get(m).get('blue')
        self.mode_chips_green = data.modes.get(m).get('green')
        self.mode_chips_brown = data.modes.get(m).get('brown')
        self.mode_chips_white = data.modes.get(m).get('white')
        self.mode_chips_gold = data.modes.get(m).get('gold')
        self.mode_nobles = data.modes.get(m).get('nobles')
    def initialize_base_board(self):
        """ Method for building a base board. This may go away 
        as the game progresses. Mainly for setting up framework
        for visualization.

        Builds a dictionary with all of the variables necessary to 
        call the render method on the jinja2 template.
        """
        base_board = {
            'chips_red': self.stack_chips_red.render(),
            'stack_large': '{:15}'.format('stacklarge'),
            'card_large_1': self.cards_large_active.pull_and_render_card(),
            'card_large_2': self.cards_large_active.pull_and_render_card(),
            'card_large_3': self.cards_large_active.pull_and_render_card(),
            'card_large_4': self.cards_large_active.pull_and_render_card(),
            'chips_white': self.stack_chips_white.render(),
            'stack_medium': '{:15}'.format('stackmedium'),
            'card_medium_1': self.cards_medium_active.pull_and_render_card(),
            'card_medium_2': self.cards_medium_active.pull_and_render_card(),
            'card_medium_3': self.cards_medium_active.pull_and_render_card(),
            'card_medium_4': self.cards_medium_active.pull_and_render_card(),
            'chips_blue': self.stack_chips_blue.render(),
            'stack_small': '{:15}'.format('stacksmall'),
            'card_small_1': self.cards_large_active.pull_and_render_card(),
            'card_small_2': self.cards_large_active.pull_and_render_card(),
            'card_small_3': self.cards_large_active.pull_and_render_card(),
            'card_small_4': self.cards_large_active.pull_and_render_card(),
            'chips_brown': self.stack_chips_brown.render(),
            'chips_green': self.stack_chips_green.render(),
            'chips_gold': self.stack_chips_gold.render(),
            'nobles': self.nobles.render(),
            'player_1': 'p1',
            'player_2': 'p2',
            'player_3': 'p3',
            'player_4': 'p4',
            }
        return base_board
    def cards_classify_sizes(self):
        """ Build lists of Card() objects based
        on their size class.
        """
        for card in self.cards_inventory.cards:
            if card.size == 'small':
                self.cards_small_active.cards.append(card)
                self.cards_small_active.size = 'small'
            elif card.size == 'medium':
                self.cards_medium_active.cards.append(card)
                self.cards_medium_active.size = 'medium'
            elif card.size == 'large':
                self.cards_large_active.cards.append(card)
                self.cards_large_active.size = 'large'

    def shuffle_all(self,list_of_cardstacks):
        for cardstack in list_of_cardstacks:
            random.shuffle(cardstack.cards)