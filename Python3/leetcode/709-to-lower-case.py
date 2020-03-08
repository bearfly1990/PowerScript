class Solution:
    def toLowerCase(self, str):
        """
        :type str: str
        :rtype: str
        """
        return str.lower()


tc = Solution().toLowerCase("ABC")
assert tc == 'abc', '{}==ABC'.format(tc)
