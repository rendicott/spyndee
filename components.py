import dat
import random
from jinja2 import Template
from TableFormat import TableFormat

class Noble():
    """ Basic class for a noble card.
    """
    def __init__(self,**kwargs):
        self.uid = kwargs.get('uid')
        self.points = kwargs.get('points')
        self.green = kwargs.get('green')
        self.blue = kwargs.get('blue')
        self.white = kwargs.get('white')
        self.red = kwargs.get('red')
        self.brown = kwargs.get('brown')
    def render(self):
        """ Render method that returns a formatted string.
        """
        fmt = "{0:1}({1:5}{2:5}{3:5}{4:5}{5:5})"
        props = [self.points,self.green,self.white,self.blue,self.brown,self.red]
        pnew = []
        for i,p in enumerate(props):
            msg = ''
            if p != 0:
                if i == 1:
                    msg += 'gr-%s' % str(p)
                elif i == 2:
                    msg += 'wh-%s' % str(p)
                elif i == 3:
                    msg += 'bl-%s' % str(p)
                elif i == 4:
                    msg += 'br-%s' % str(p)
                elif i == 5:
                    msg += 'rd-%s' % str(p)
                elif i == 0 or i == 1:
                    msg = p
            else:
                msg = ''
            pnew.append(msg)
        props_str = [str(x) for x in pnew]
        return '{:35}'.format(fmt.format(*props_str))


class Nobles():
    def __init__(self,quantity):
        self.nobles_inventory = []
        self.nobles_active = []
    def load_nobles(self,data):
        for noble in data:
            n = Noble(uid=noble,
                      points=data.get(noble).get('points'),
                      green=data.get(noble).get('green'),
                      blue=data.get(noble).get('blue'),
                      white=data.get(noble).get('white'),
                      red=data.get(noble).get('red'),
                      brown=data.get(noble).get('brown'),
                    )
            self.nobles_inventory.append(n)
    def shuffle_build_active(self,quantity):
        shuffled = list(self.nobles_inventory)
        random.shuffle(shuffled)
        self.nobles_active = shuffled[0:quantity]
    def render(self):
        """ Render method that returns a list of formatted strings.
        """
        results = [x.render() for x in self.nobles_active]
        return results


class Chips():
    def __init__(self,color,color_short_name,total):
        self.color = color
        self.color_short_name = color_short_name
        self.total = int(total)
        self.remaining = int(self.total)
    def take_chip(self):
        if self.remaining >= 1:
            self.remaining -= 1
            return True
        else:
            return False
    def return_chip(self):
        if self.remaining < self.total:
            self.remaining += 1
            return True
        else:
            return False
    def render(self):
        """ Render method that returns a formatted string.
        """
        msg = '{0:2}-{1:2}'.format(self.color_short_name,self.remaining)
        return msg


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
        """ A method for displaying this card's
        data in a table format using the TableFormat library
        Mainly for development and debugging.
        """
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
        """ A method for displaying this card's header
        data in a table format using the TableFormat library
        Mainly for development and debugging.
        """
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
        """ Render method that returns a formatted string.
        """
        fmt = "{0:6}{1:2} ({2:5}{3:5}{4:5}{5:5}{6:5})"
        props = [self.iden,self.points,self.green,self.white,self.blue,self.brown,self.red]
        pnew = []
        for i,p in enumerate(props):
            msg = ''
            # based on the position of the property we know which color it is, yuck
            if p != 0:
                if i == 2:
                    msg += 'gr-%s' % str(p)
                elif i == 3:
                    msg += 'wh-%s' % str(p)
                elif i == 4:
                    msg += 'bl-%s' % str(p)
                elif i == 5:
                    msg += 'br-%s' % str(p)
                elif i == 6:
                    msg += 'rd-%s' % str(p)
                elif i == 0 or i == 1:
                    msg = p
            else:
                msg = ''
            pnew.append(msg)
        props_str = [str(x) for x in pnew]
        return '{:40}'.format(fmt.format(*props_str))
                

class Cards():
    """ Class for structuring a stack of Card() objects.
    Methods will include things like shuffle, popping cards,
    and handling end of stack and remaining cards, etc.
    """
    def __init__(self):
        self.cards = []
        self.cards_small = []
        self.cards_medium = []
        self.cards_large = []
    def cards_classify_sizes(self):
        """ Build lists of Card() objects based
        on their size class.
        """
        for card in self.cards:
            if card.size == 'small':
                self.cards_small.append(card)
            elif card.size == 'medium':
                self.cards_medium.append(card)
            elif card.size == 'large':
                self.cards_large.append(card)
    def stats_color_spread(self):
        """ Method for getting some card statistics. 
        This is just interesting to see and not used
        in gameplay.
        """
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
        """ Method for getting some card statistics. 
        This is just interesting to see and not used
        in gameplay.
        """
        avg_cost = 0
        total_cost = sum(x.cost_total() for x in getattr(self,lister))
        try:
            avg_cost = float(total_cost) / float(len(getattr(self,lister)))
        except:
            pass
        return avg_cost
    def stats_cost(self):
        """ Method for getting some card statistics. 
        This is just interesting to see and not used
        in gameplay.
        """
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
        """ Method for dumping all cards in a table format for 
        development debugging. 
        """
        msg = (self.cards[0].tableformat_header() + '\n')
        for card in self.cards:
            msg += (card.dumpself_tableformat() + '\n')
        return msg
    def load_cards(self,data):
        """ Method for loading cards from the data file.
        """
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
                self.cards.append(n)





