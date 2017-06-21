""" This is the main method. Used to orchestrate
the building of the board and components.
"""
import unittest
import components
import dat
import board

num_players = 4

def show_statistics(board):
    print(board.cards_inventory.stats_color_spread())
    board.cards_classify_sizes()
    print(board.stats_cost())
    print(board.cards_inventory.dumpself_cards())

def main():

    # build a Board() class with custom data for this session
    b = board.Board(num_players,dat)

    # if you want you can see some debug stats about the board
    show_statistics(b)

    # give a quick display of the generated board
    #print b.render()

if __name__ == '__main__':
    #unittest.main()  
    main()