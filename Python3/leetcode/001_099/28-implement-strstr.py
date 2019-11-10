import time
class Solution:
    def strStr(self, haystack, needle):
        """
        :type haystack: str
        :type needle: str
        :rtype: int
        """
        if len(needle) == 0:
            return 0
        i = 0
        j = 0
        while i < len(haystack):
            if haystack[i] == needle[j]:
                i = i + 1
                j = j + 1
            else:
                i = i - j + 1
                j = 0
            if j == len(needle):
                return i - len(needle)
        return -1
        # return haystack.find(needle)

tc = Solution().strStr("hello", "ll")
assert tc == 2, '{}==2'.format(tc)

tc = Solution().strStr("aaaaa", "bba")
assert tc == -1, '{}==-1'.format(tc)

tc = Solution().strStr("mississippi", "issip")
assert tc == 4, '{}==4'.format(tc)

tc = Solution().strStr("mississippi", "")
assert tc == 0, '{}==0'.format(tc)

tc = Solution().strStr("a", "a")
assert tc == 0, '{}==0'.format(tc)


