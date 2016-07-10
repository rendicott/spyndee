import dat
from TableFormat import TableFormat
from termcolor import colored

class Noble():
    def __init__(self,**kwargs):
        self.uid = kwargs.get('uid')
        self.points = kwargs.get('points')
        self.green = kwargs.get('green')
        self.blue = kwargs.get('blue')
        self.white = kwargs.get('white')
        self.red = kwargs.get('red')
        self.brown = kwargs.get('brown')

class Nobles():
    def __init__(self):
        self.nobles = []

class Card():
    def __init__(self,**kwargs):
        self.uid = kwargs.get('uid')
        self.size = kwargs.get('size')
        self.iden = kwargs.get('iden')
        self.points = kwargs.get('points')
        self.green = kwargs.get('green')
        self.blue = kwargs.get('blue')
        self.white = kwargs.get('white')
        self.red = kwargs.get('red')
        self.brown = kwargs.get('brown')
        self.dump_ignore_attrs = []
        self.dict_extend_values = {'iden': 7, 'size': 7}
    def cost_total(self):
        cost = (
            self.green +
            self.blue +
            self.white +
            self.red +
            self.brown 
            )
        return cost
    def dumpself_tableformat(self):
        msg = ''
        attributes = []
        values = []
        for attr in dir(self):
            if (
                    '__' not in attr and
                    'instancemethod' not in str(type(getattr(self, attr))) and
                    'dict' not in str(type(getattr(self, attr))) and
                    'dump_ignore_attrs' not in attr):
                attributes.append(attr)
                values.append(str(getattr(self, attr)))
        format_helper = TableFormat(attributes, values, self.dict_extend_values, self.dump_ignore_attrs)
        msg += format_helper.string_values
        return msg
    def tableformat_header(self):
        msg = ''
        attributes = []
        values = []
        for attr in dir(self):
            if (
                    '__' not in attr and
                    'instancemethod' not in str(type(getattr(self, attr))) and
                    'dict' not in str(type(getattr(self, attr))) and
                    'dump_ignore_attrs' not in attr):
                attributes.append(attr)
                values.append(str(getattr(self, attr)))
        format_helper = TableFormat(attributes, values, self.dict_extend_values, self.dump_ignore_attrs)
        msg += format_helper.string_header
        return msg
    def render_card(self):
        template = """
         ---------
        | {0}     {1} |
        |         |
        |         |
        | {2} {3} {4}   |
        | {5} {6}     |
         ---------
        """
        mappings = {
            0: 'points',
            1: 'iden',
            2: 'green',
            3: 'white',
            4: 'blue',
            5: 'brown',
            6: 'red',
        }
        if self.points != 0:
            cpoints = self.points
        else:
            cpoints = ' '

        if self.iden == 'green':
            ciden = colored('*','white','on_green')
        elif self.iden == 'red':
            ciden = colored('*','white','on_red')
        elif self.iden == 'white':
            ciden = colored('*','white','on_white')
        elif self.iden == 'blue':
            ciden = colored('*','white','on_blue')
        elif self.iden == 'brown':
            ciden = colored('*','red','on_yellow')

        if self.green != 0:
            cgreen = colored(str(self.green),'green')
        else:
            cgreen = ' '

        if self.red != 0:
            cred = colored(str(self.red),'white','on_red')
        else:
            cred = ' '

        if self.white != 0:
            cwhite = colored(str(self.white),'white')
        else:
            cwhite = ' '

        if self.blue != 0:
            cblue = colored(str(self.blue),'white','on_blue')
        else:
            cblue = ' '

        if self.brown != 0:
            cbrown = colored(str(self.brown),'yellow')
        else:
            cbrown = ' '

        values = [cpoints,ciden,cgreen,cwhite,cblue,cbrown,cred]
        msg = template.format(*values)
        return msg
                

class Cards():
    def __init__(self):
        self.cards = []
        self.cards_small = []
        self.cards_medium = []
        self.cards_large = []
    def cards_classify_sizes(self):
        for card in self.cards:
            if card.size == 'small':
                self.cards_small.append(card)
            elif card.size == 'medium':
                self.cards_medium.append(card)
            elif card.size == 'large':
                self.cards_large.append(card)
    def stats_color_spread(self):
        msg = "---COLOR IDENTITY SPREAD ALL CARDS--\n"
        cgreen = 0
        cblue = 0
        cwhite = 0
        cred = 0
        cbrown = 0
        for card in self.cards:
            if card.iden == 'green':
                cgreen += 1
            elif card.iden == 'blue':
                cblue += 1
            elif card.iden == 'white':
                cwhite += 1
            elif card.iden == 'red':
                cred += 1
            elif card.iden == 'brown':
                cbrown += 1
        header = ['green','blue','white','red','brown']
        fmt = '{0:6}{1:6}{2:6}{3:6}{4:6}\n'
        content = [cgreen,cblue,cwhite,cred,cbrown]
        content_str = [str(x) for x in content]
        msg += fmt.format(*header)
        msg += fmt.format(*content_str)
        return(msg)
    def stats_avg_cost(self,lister):
        avg_cost = 0
        total_cost = sum(x.cost_total() for x in getattr(self,lister))
        try:
            avg_cost = float(total_cost) / float(len(getattr(self,lister)))
        except:
            pass
        return avg_cost
    def stats_cost(self):
        msg = "----AVG # OF CHIPS COST PER CARD CATEGORY---\n"
        self.cards_classify_sizes()
        avg_cost_all = self.stats_avg_cost('cards')
        avg_cost_small = self.stats_avg_cost('cards_small')
        avg_cost_medium = self.stats_avg_cost('cards_medium')
        avg_cost_large = self.stats_avg_cost('cards_large')

        fmt = "{0:7}{1:7}{2:7}{3:7}\n"
        header = ['small','medium','large','all']
        content = [avg_cost_small,avg_cost_medium,avg_cost_large,avg_cost_all]
        content_str = [str('{:.2f}'.format(x)) for x in content]

        msg += fmt.format(*header)
        msg += fmt.format(*content_str)

        return(msg)
    def dumpself_cards(self):
        msg = (self.cards[0].tableformat_header() + '\n')
        for card in self.cards:
            msg += (card.dumpself_tableformat() + '\n')
        return msg



def load_nobles(data):
    ns = Nobles()
    for noble in data:
        n = Noble(uid=noble,
                  points=data.get(noble).get('points'),
                  green=data.get(noble).get('green'),
                  blue=data.get(noble).get('blue'),
                  white=data.get(noble).get('white'),
                  red=data.get(noble).get('red'),
                  brown=data.get(noble).get('brown'),
                )
        ns.nobles.append(n)
    return ns

def load_cards(data):
    cs = Cards()
    for size in data:
        for card in data.get(size):
            n = Card(uid=card,
                     iden=data.get(size).get(card).get('iden'),
                     size=size,
                     points=data.get(size).get(card).get('points'),
                     green=data.get(size).get(card).get('green'),
                     blue=data.get(size).get(card).get('blue'),
                     white=data.get(size).get(card).get('white'),
                     red=data.get(size).get(card).get('red'),
                     brown=data.get(size).get(card).get('brown'),
                    )
            cs.cards.append(n)
    return cs