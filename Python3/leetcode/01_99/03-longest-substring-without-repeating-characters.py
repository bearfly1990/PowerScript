class Solution:
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        left = 0
        right = 0
        char_map = {}
        max_len = 0
        while right < len(s):
            if char_map.get(s[right]) is None:
                char_map[s[right]] = right
            else:
                left = max(left, char_map[s[right]]+1)
                char_map[s[right]] = right
            max_len = max(max_len, right - left + 1)
            # print(left, right, s[right], char_map, max_len)
            right = right + 1
        return max_len


tc = Solution().lengthOfLongestSubstring("pwwkew")
assert tc == 3, '{}==3'.format(tc)

tc = Solution().lengthOfLongestSubstring("bbbbb")
assert tc == 1, '{}==1'.format(tc)

tc = Solution().lengthOfLongestSubstring("abcabcbb")
assert tc == 3, '{}==3'.format(tc)

tc = Solution().lengthOfLongestSubstring("dvdf")
assert tc == 3, '{}==3'.format(tc)
