class Solution:
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        brackets_map = {'(': ')', '{': '}', '[': ']', '#':'#'}
        stack_left = ['#']
        for i in range(len(s)):
            if s[i] in brackets_map.keys():
                stack_left.append(s[i])
            elif s[i] in brackets_map.values():
                bracket_left = stack_left.pop()
                if (brackets_map[bracket_left] != s[i]):
                    return False
        if stack_left.pop() != '#':
            return False
        return True

assert Solution().isValid("[") == False    
assert Solution().isValid("]") == False
assert Solution().isValid("()[]{}") == True
assert Solution().isValid("{[]}") == True
assert Solution().isValid("([)]") == False
