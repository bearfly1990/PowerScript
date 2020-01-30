class Solution:
    def sortedSquares(self, A):
        """
        :type A: List[int]
        :rtype: List[int]
        """
        new_squared_array = [x * x for x in A]
        new_squared_array.sort()
        return new_squared_array

tc = Solution().sortedSquares([-7,-3,2,3,11])
assert tc == [4,9,9,49,121], '{}==[4,9,9,49,121]'.format(tc)

