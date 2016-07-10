import loader
import dat
from termcolor import cprint

ns = loader.load_nobles(dat.nobles)
cs = loader.load_cards(dat.cards)

cs.cards_classify_sizes()
print(cs.stats_color_spread())
print(cs.stats_cost())

print(cs.dumpself_cards())

for i,card in enumerate(cs.cards):
    print card.render_card() 