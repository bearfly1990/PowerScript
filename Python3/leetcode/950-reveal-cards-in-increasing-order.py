from collections import deque
class Solution:
    def deckRevealedIncreasing(self, deck):
        """
        :type deck: List[int]
        :rtype: List[int]
        """
        deck.sort(reverse=True)
        car_deque = deque()
        popped = None
        for i in range(len(deck)):
            if len(car_deque) > 0:
                popped = car_deque.pop()
            if popped:
                car_deque.appendleft(popped)
            car_deque.appendleft(deck[i])
        return list(car_deque)

tc = Solution().deckRevealedIncreasing([17,13,11,2,3,5,7])
assert tc == [2,13,3,11,5,17,7], '{}==[2,13,3,11,5,17,7]'.format(tc)

