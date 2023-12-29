RANK = {"1": 2, "2": 3, "3": 4, "4": 5, "5": 6, "6": 7, "7": 8,
        "8": 9, "9": 10, "T": 11, "J": 1, "Q": 12, "K": 13, "A": 14}


def has_full_house(hand_string: str, d=False):
    three1, _, ex1 = has_n_of_a_kind(hand_string, 3, True)
    pair1, _, c2 = has_n_of_a_kind(hand_string, 2, False, ex1)

    three2, _, ex2 = has_n_of_a_kind(hand_string, 3, True)
    pair2, _, c4 = has_n_of_a_kind(hand_string, 2, False, ex2)
    if (d):
        print(three1, pair1, three2, pair2, ex1, c2, ex2, c4)
    return (three1 and pair1) or (three2 and pair2)


def has_n_of_a_kind_1(hand_string: str, n: int):
    success = False
    matches = 0
    counted = set()
    for c in hand_string:
        if hand_string.count(c) == n and c not in counted:
            counted.add(c)
            matches += 1
            success = True
    return success, matches


def has_n_of_a_kind(hand_string: str, n: int, check_js=True, exclude=None):
    if exclude is None:
        exclude = set()
    success = False
    matches = 0
    counted = set()
    for c in hand_string:
        if c not in exclude and (hand_string.count(c) + (hand_string.count('J') if check_js and c != 'J' else 0)) == n and c not in counted:
            counted.add(c)
            matches += 1
            success = True
    if n == 2 and 'J' in hand_string:
        matches = 1
    # The bug is here, matches is too high if there's a J
    return success, matches, counted


def has_high_card(hand_string: str):
    return max(RANK[c] for c in hand_string)


def get_hand_rank(hand_string):
    return [RANK[c] for c in hand_string]


def get_tie_score(hand_string):
    l = len(hand_string)
    score = 0
    for i, c in enumerate(hand_string):
        score += RANK[c] * 1000 ** (l-i)
    return score


def parse(raw_data):
    return [line.strip().split(' ') for line in raw_data.split('\n')]


def solve1(data):
    hand_scores = {}
    tie_scores = {}
    hand_bets = {}
    for hand, bet in data:
        bet = int(bet)
        hand_bets[hand] = bet
        tie_scores[hand] = get_tie_score(hand)

        five, _, __ = has_n_of_a_kind(hand, 5)
        if five:
            hand_scores[hand] = 1000 ** 6
            continue
        four, _, __ = has_n_of_a_kind(hand, 4)
        if four:
            hand_scores[hand] = 1000 ** 5
            continue
        full_house = has_full_house(hand)
        if full_house:
            hand_scores[hand] = 1000 ** 4
            continue
        three, _, __ = has_n_of_a_kind(hand, 3)
        if three:
            hand_scores[hand] = 1000 ** 3
            continue
        pairs, n_pairs, _ = has_n_of_a_kind(hand, 2)
        if pairs:
            hand_scores[hand] = 1000 ** n_pairs
            continue
        hand_scores[hand] = 0

    sorted_scores = list(
        sorted(hand_scores, key=lambda x: (hand_scores[x], tie_scores[x])))

    total_score = sum(hand_bets[score] * (i + 1)
                      for i, score in enumerate(sorted_scores))
    return total_score


def solve2(data):
    hand_scores = {}
    tie_scores = {}
    hand_bets = {}
    for hand, bet in data:
        j_count = hand.count('J')
        hand_noj = hand.replace('J', "")
        bet = int(bet)
        hand_bets[hand] = bet
        tie_scores[hand] = get_tie_score(hand)

        five, _, __ = has_n_of_a_kind(hand_noj, 5)
        if five:
            hand_scores[hand] = 1000 ** 6
            continue
        four, _, __ = has_n_of_a_kind(hand_noj, 4)
        if four:
            hand_scores[hand] = 1000 ** min(6, 5 + j_count)
            continue
        full_house = has_full_house(hand_noj)
        if full_house:
            hand_scores[hand] = 1000 ** 4
            continue
        three, _, __ = has_n_of_a_kind(hand_noj, 3)
        if three:
            hand_scores[hand] = 1000 ** min(6, 3 +
                                            j_count + (1 if j_count > 0 else 0))
            continue
        pairs, n_pairs, _ = has_n_of_a_kind(hand_noj, 2)
        if pairs:
            if n_pairs == 2 and j_count == 1:
                hand_scores[hand] = 1000 ** 4  # full house
            else:  # n_pairs should be 1
                j_factor = j_count
                if j_factor > 0:
                    j_factor += 1
                if j_factor + n_pairs >= 4:
                    j_factor += 1

                hand_scores[hand] = 1000 ** min(6, j_factor + n_pairs)
            continue
        j_factor = j_count
        if j_factor >= 2:
            j_factor += 1
        if j_factor >= 4:
            j_factor += 1
        hand_scores[hand] = 1000 ** min(6, j_factor)

    sorted_scores = list(
        sorted(hand_scores, key=lambda x: (hand_scores[x], tie_scores[x])))
    for s in sorted_scores:
        print(s, hand_scores[s], hand_bets[s])
    total_score = sum(hand_bets[score] * (i + 1)
                      for i, score in enumerate(sorted_scores))
    return total_score


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
