class Solution:
    def longestPalindrome(self, s: str) -> str:
        if self.isPalindrome(s):
            return s
        max_s = s[0]
        for i in range(len(s)):
            max_s = max (self.spread(s, i, i), self.spread(s, i, i + 1), max_s, key=len)
        return max_s

    def isPalindrome(self, s: str) -> bool:
        return s == s[::-1]

    def spread(self, s: str, left: int, right:int) -> str:
        while (left >=0 and right < len(s) and s[left] == s[right]):
            left = left - 1
            right = right + 1
        return s[left+1: right] 



tc = Solution().longestPalindrome('babad')
print(tc)
