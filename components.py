import dat
import random
import unittest
import copy
from jinja2 import Template
from TableFormat import TableFormat

register = {'gold': 0,
            'red': 0,
            'green': 0,
            'brown': 0,
            'blue': 0,
            'white': 0,
            }

mappings_shortnames = {
            'green': 'gr-',
            'white': 'wh-',
            'blue': 'bl-',
            'brown': 'br-',
            'red': 'rd-',
            'gold': 'go-'
            }

class PlayerBank():

    def __init__(self):
        # set up purchase power registers
        self.pp_chips = copy.deepcopy(register)
        self.pp_deck = copy.deepcopy(register)
        self.pp_total = copy.deepcopy(register)
    def has_three_gold(self):
        # returns True if player already has three gold
        # false otherwise
        if self.pp_chips.get('gold') >= 3:
            return True
        else:
            return False

    def add_chip(self,color=None,quantity=None):
        if quantity == None:
            quantity = 1
        for p in self.pp_chips:
            if p == color:
                self.pp_chips[p] += quantity
        self.recount()

    def recount(self):
        for p in self.pp_chips:
            self.pp_total[p] = self.pp_chips[p] + self.pp_deck[p]

    def allocate_gold(self,missing):
        ''' Based on what chips are missing we allocate what
        gold we have. Returns a register with the amount of
        each color to allocate with gold or returns None
        if this is not possible.
        '''
        # if total missing chip cost is greater than the amount of gold we have
        #  then we definately can't afford.
        sum_of_missing = sum([x for x in missing.itervalues()])
        print("SUM OF MISSING: " + str(sum_of_missing))
        print("TOTAL GOLD: " + str(self.pp_total['gold']))
        if sum_of_missing > self.pp_total['gold']:
            return None
        # make a gold allocation register
        gar = copy.deepcopy(register)
        # take a copy of current gold so we don't actually take it
        goldcount = copy.deepcopy(self.pp_total['gold'])
        # keep a rotation count to protect from loops
        rotations = 0
        while sum_of_missing > 0 or goldcount > 0:
            for color in missing:
                if missing[color] > 0:
                    gar[color] += 1
                    goldcount -= 1
                    missing[color] -= 1
            rotations += 1
            if rotations > 20:
                print("OHNO<>TOOMANYROTATATIONS")
                break
        return gar

    def can_afford(self,card,return_missing=None):
        ''' Determines if a given card is affordable
        by the player taking deck cards as well as
        gold/wild chips into consideration. Returns
        True or False. If the return_missing boolean
        is set then a register of missing chips is
        returned instead of a boolean.
        '''
        if return_missing is None:
            return_missing = False
        # find the properties of the card object that contain colors
        color_props = [x for x in dir(card) if x in register]
        # make a new cost register dictionary 
        cost_register = copy.deepcopy(register)
        # populate register with cost properties from card
        for prop in color_props:
            cost_register[prop] = getattr(card,prop)
        # default to afford False
        can_afford = False
        needs_gold = False
        missing = {}
        # loop through current purchase power and find out what's missing
        for p in self.pp_total:
            if self.pp_total.get(p) < cost_register.get(p):
                missing[p] = cost_register.get(p) - self.pp_total.get(p)
        print("MISSING: " + str(missing))
        if return_missing:
            return missing
        # if what's missing adds up to < 0 then we can definately afford
        print("GAR: " + str(self.allocate_gold(missing)))
        if sum([x for x in missing.itervalues()]) <= 0:
            can_afford = True
            needs_gold = False
        elif self.allocate_gold(missing) is not None:
            can_afford = True
            needs_gold = True
        else:
            can_afford = False
            needs_gold = False
        return can_afford, needs_gold
        
        return(can_afford)
    def purchase_card(self,card):
        return_value = False
        can_afford, needs_gold = self.can_afford(card)
        print("CAN_AFFORD: %s, NEEDS_GOLD: %s" % (can_afford,needs_gold))
        if can_afford:
            try:
                color_props = [x for x in dir(card) if x in register]
                cost_register = copy.deepcopy(register)
                for prop in color_props:
                    cost_register[prop] = getattr(card,prop)
                # modify the cost register based on how many deck cards
                for p in cost_register:
                    cost_register[p] -= self.pp_deck.get(p)
                    if cost_register[p] < 0:
                        cost_register[p] = 0
                # now take the rest from chips
                for p in cost_register:
                    while self.pp_chips[p] >= 1 and cost_register[p] >= 1:
                        self.pp_chips[p] -= 1
                        cost_register[p] -= 1

                    
                remaining_cost = sum([x for x in cost_register.itervalues()])
                print("REMAINING_COST: %s" % str(remaining_cost))
                if needs_gold and remaining_cost > 0:
                    missing = self.can_afford(card, return_missing=True)
                    gar = self.allocate_gold(card,missing)
                    # now go through the gold allocation register and subtract from gold
                    for color in gar:
                        self.pp_total['gold'] -= gar[color]
                        cost_register[color] -= gar[color]
                    if self.pp_total['gold'] < 0:  # there was a problem
                        return_value = False
                # make sure cost_register is empty
                if remaining_cost > 0:
                    return_value = False
                else:
                    return_value = True
            except Exception as e:
                msg = ("Exception in purchase_card: " + str(e))
                return_value = False
                print(msg)
            # now add value of iden to pp_deck if everything is good
            if return_value:
                for p in self.pp_deck:
                    if p == card.iden:
                        self.pp_deck[p] += 1
        self.recount()
        return return_value
    def render(self):
        fmt = '( {0:5}{1:5}{2:5}{3:5}{4:5}{5:5})'
        rows = {}
        for j,pp_register in enumerate([self.pp_deck, self.pp_chips, self.pp_total]):
            vals = []
            for i,key in enumerate(pp_register):
                val = pp_register.get(key)
                sn = ''
                for mapping in mappings_shortnames:
                    if mapping == key:
                        sn = mappings_shortnames.get(mapping)
                vals.append('%s%s' % (sn,val))
            if j == 0:
                # means it's deck which needs no gold 
                vals[vals.index('go-0')] = '    '
            current_row = 'row' + str(j)
            rows[current_row] = fmt.format(*vals)
        jtpl_msg = """
deck : {{row0}}
chips: {{row1}}
total: {{row2}}
        """
        tpl = Template(jtpl_msg)
        return(str(tpl.render(rows)))




class Player():
    def __init__(self,data):
        self.name = 'bob'
        self.deck = []
        self.reserved = []
        self.points = 0
        self.bank = PlayerBank()
        self.points_to_win = data.points_to_win
        self.max_tokens_in_hand = data.max_tokens_in_hand
        self.max_reserve_cards = data.max_reserve_cards
    def takes_card(self,card):
        can_afford, needs_gold = self.bank.can_afford(card)
        if can_afford:
            if self.bank.purchase_card(card):
                self.deck.append(card)
        elif not can_afford and len(self.reserved) < self.max_reserve_cards:
            if not self.bank.has_three_gold():
                self.reserved.append(card)
                self.bank.add_chip(color='gold')
            else:
                msg = "ERROR TOO MANY GOLD"
                print(msg)
    def takes_chip(self,color):
        if not color == 'gold':
            self.bank.add_chip(color)
        else:
            msg = "ERROR, MUST RESERVE CARD TO GET A GOLD"
            print(msg)
    def render(self):
        jtpl_msg = """
{{name}} 
{{bank}}"""
        bank = self.bank.render()
        tpl = Template(jtpl_msg)
        return str(tpl.render(name=self.name, bank=bank))


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

class ChipsAll():
    def __init__(self):
        self.stacks = []


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
    def render(self):
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
        self.size = ''

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
    def pull_and_render_card(self):
        r = self.cards.pop()
        return r.render()
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
    def stats_avg_cost(self):
        """ Method for getting some card statistics. 
        This is just interesting to see and not used
        in gameplay.
        """
        avg_cost = 0
        total_cost = sum(x.cost_total() for x in self.cards)
        try:
            avg_cost = float(total_cost) / float(len(self.cards))
        except:
            pass
        return avg_cost



class Dummy_Old():
    def __init__(self):
        pass
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

