# Used to shuffle generated decks.
from random import shuffle

# Unit test suite.
import unittest


# Used to permute the suits and values of cards.
SUITS = ['D', 'C', 'H', 'S']
VALUES = range(1, 14)
FLOP_SIZE = 5


def make_deck():
    '''
    Makes a list containing all of the cards in list, shuffled.
    '''
    # Create the deck.
    deck = []
    for value in VALUES:
        for suit in SUITS:
            deck.append((value, suit))
    # Return the deck.
    shuffle(deck)
    return deck


def get_values(cards):
    '''
    Strips the suit from the cards.
    '''
    return [card[0] for card in cards]


def get_count(cards):
    '''
    Returns a list containing the value counts of the cards.
    '''
    # Get the values from the cards.
    values = get_values(cards)

    # Get the counts from the values list. We should have a total of
    # 10 cards.
    count = []
    for value in list(set(values)):
        count.append(values.count(value))

    return count


def is_pair(cards):
    '''
    Returns true if a single pair is found.
    '''
    count = get_count(cards)
    return count.count(2) == 1 and count.count(3) == 0 and count.count(4) == 0


def is_triple(cards):
    '''
    Returns true if a triple is found.
    '''
    count = get_count(cards)
    return count.count(3) == 1 or count.count(3) == 2


def is_quad(cards):
    '''
    Returns true if a quad is found.
    '''
    count = get_count(cards)
    return count.count(4) == 1


def is_two_pair(cards):
    '''
    Returns true if a quad is found.
    '''
    count = get_count(cards)
    return count.count(2) == 2 and count.count(3) == 0 or count.count(2) == 3


def permute_draw(deck, draw):
    '''
    Returns a list containing a list of permuted flops.
    '''
    # Sanity check.
    assert(draw > 0)

    # Check to see if we're at the last card drawn.
    if draw == 1:
        result = []
        for card in deck:
            result.append([card])
        return result

    # Check to see if we can still make more permutations.
    if len(deck) < draw:
        return []

    # Run the permutation and join it with the recursive result
    # of other permutations.
    result = []
    for ii in range(len(deck)):
        # Generate the permutation for the next recursion.
        next = permute_draw(deck[ii + 1:], draw - 1)

        # If there were no results, we can end early.
        if len(next) == 0:
            break

        # Append the current card to the permutation.
        for entry in next:
            entry.append(deck[ii])
            result.append(entry)

    # Return the result.
    return result


def get_my_odds(hand, flop, print_odds=False):
    '''
    Recursively brute forces the odds of the various hands.
    '''
    # Calculate the deck.
    deck = make_deck()
    for card in hand + flop:
        deck.remove(card)

    # Permute the remaining cards.
    draw = permute_draw(deck, FLOP_SIZE - len(flop))

    # Detectors for the different hand types.
    detectors = {}
    detectors['Pair'] = is_pair
    detectors['Triple'] = is_triple
    detectors['Quad'] = is_quad
    detectors['Two Pair'] = is_two_pair

    # Results for the check; initialized to zero for all detectors.
    result = {}
    for key in detectors:
        result[key] = 0

    # Count the number of hand types.
    for cards in draw:
        # Get the full set of cards.
        cards += hand + flop

        # Run the cards over the set of detectors.
        for key in detectors:
            if detectors[key](cards):
                result[key] += 1

    # Print the results.
    for key in result:
        # Calculate the probabilities.
        value = result[key]
        total = len(draw)
        probability = float(value) / float(total)

        # Display the results.
        if print_odds:
            print('%s: %s in %s' % (key, value, total))
        else:
            print('%s: %s' % (key, probability))


class testCases(unittest.TestCase):
    def testIsPair(self):
        # Test a real pair.
        hand = [(1, 'H'), (13, 'S')]
        flop = [(2, 'C'), (6, 'S'), (1, 'S'), (5, 'D')]
        self.assertTrue(is_pair(hand + flop))

        # Test triples.
        hand = [(1, 'H'), (13, 'S')]
        flop = [(1, 'C'), (6, 'S'), (1, 'S')]
        self.assertFalse(is_pair(hand + flop))

        # Test quads.
        hand = [(1, 'H'), (13, 'S')]
        flop = [(1, 'C'), (6, 'S'), (1, 'S'), (1, 'D')]
        self.assertFalse(is_pair(hand + flop))

        # Test two pair.
        hand = [(1, 'H'), (13, 'S')]
        flop = [(2, 'C'), (6, 'S'), (1, 'S'), (5, 'D'), (5, 'H')]
        self.assertFalse(is_pair(hand + flop))

        # Test card high.
        hand = [(1, 'H'), (13, 'S')]
        flop = [(2, 'C'), (6, 'S'), (3, 'S'), (5, 'D')]
        self.assertFalse(is_pair(hand + flop))

    def testIsTriple(self):
        # Test a real pair.
        hand = [(1, 'H'), (13, 'S')]
        flop = [(2, 'C'), (6, 'S'), (1, 'S'), (5, 'D')]
        self.assertFalse(is_triple(hand + flop))

        # Test triples.
        hand = [(1, 'H'), (13, 'S')]
        flop = [(1, 'C'), (6, 'S'), (1, 'S')]
        self.assertTrue(is_triple(hand + flop))

        # Test quads.
        hand = [(1, 'H'), (13, 'S')]
        flop = [(1, 'C'), (6, 'S'), (1, 'S'), (1, 'D')]
        self.assertFalse(is_triple(hand + flop))

        # Test two pair.
        hand = [(1, 'H'), (13, 'S')]
        flop = [(2, 'C'), (6, 'S'), (1, 'S'), (5, 'D'), (5, 'H')]
        self.assertFalse(is_triple(hand + flop))

        # Test card high.
        hand = [(1, 'H'), (13, 'S')]
        flop = [(2, 'C'), (6, 'S'), (3, 'S'), (5, 'D')]
        self.assertFalse(is_triple(hand + flop))

    def testIsQuad(self):
        # Test a real pair.
        hand = [(1, 'H'), (13, 'S')]
        flop = [(2, 'C'), (6, 'S'), (1, 'S'), (5, 'D')]
        self.assertFalse(is_quad(hand + flop))

        # Test triples.
        hand = [(1, 'H'), (13, 'S')]
        flop = [(1, 'C'), (6, 'S'), (1, 'S')]
        self.assertFalse(is_quad(hand + flop))

        # Test quads.
        hand = [(1, 'H'), (13, 'S')]
        flop = [(1, 'C'), (6, 'S'), (1, 'S'), (1, 'D')]
        self.assertTrue(is_quad(hand + flop))

        # Test two pair.
        hand = [(1, 'H'), (13, 'S')]
        flop = [(2, 'C'), (6, 'S'), (1, 'S'), (5, 'D'), (5, 'H')]
        self.assertFalse(is_quad(hand + flop))

        # Test card high.
        hand = [(1, 'H'), (13, 'S')]
        flop = [(2, 'C'), (6, 'S'), (3, 'S'), (5, 'D')]
        self.assertFalse(is_quad(hand + flop))

    def testIsTwoPair(self):
        # Test a real pair.
        hand = [(1, 'H'), (13, 'S')]
        flop = [(2, 'C'), (6, 'S'), (1, 'S'), (5, 'D')]
        self.assertFalse(is_two_pair(hand + flop))

        # Test triples.
        hand = [(1, 'H'), (13, 'S')]
        flop = [(1, 'C'), (6, 'S'), (1, 'S')]
        self.assertFalse(is_two_pair(hand + flop))

        # Test quads.
        hand = [(1, 'H'), (13, 'S')]
        flop = [(1, 'C'), (6, 'S'), (1, 'S'), (1, 'D')]
        self.assertFalse(is_two_pair(hand + flop))

        # Test two pair.
        hand = [(1, 'H'), (13, 'S')]
        flop = [(2, 'C'), (6, 'S'), (1, 'S'), (5, 'D'), (5, 'H')]
        self.assertTrue(is_two_pair(hand + flop))

        # Test card high.
        hand = [(1, 'H'), (13, 'S')]
        flop = [(2, 'C'), (6, 'S'), (3, 'S'), (5, 'D')]
        self.assertFalse(is_two_pair(hand + flop))


if __name__ == '__main__':
    #unittest.main()

    hand = [(1, 'H'), (13, 'S')]
    #hand = [(1, 'H'), (1, 'S')]

    #flop = [(2, 'C'), (6, 'S'), (3, 'S'), (5, 'D')]
    flop = [(2, 'C'), (6, 'S'), (3, 'S')]
    #flop = []

    print('hand: %s' % str(hand))
    print('flop: %s' % str(flop))
    get_my_odds(hand, flop, print_odds=True)
