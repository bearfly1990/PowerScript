import re
class Solution:
    def countAndSay(self, n: int) -> str:
        if n == 1:
            return "1"
        pre_str = self.countAndSay(n - 1)
        count = 0
        current_char = pre_str[0]
        result = []
        temp = []
        for char in pre_str:
            if char == current_char:
                temp.append(char)
            if char != current_char:
                result.append(str(len(temp)))
                result.append(str(temp[0]))
                temp = []
                current_char = char
                temp.append(char)
        if len(temp) > 0:
            result.append(str(len(temp)))
            result.append(str(temp[0]))
        return ''.join(result)
                
                

solution = Solution()        
print(solution.countAndSay(5))