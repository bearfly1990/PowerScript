class Solution:
    def intToRoman(self, num):
        """
        :type num: int
        :rtype: str
        """
        roman_int_map = {'I': 1, 'V': 5, 'X': 10,
                         'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        new_char_map = {'IV': 4, 'IX': 9,
                       'XL': 40, 'XC': 90, 'CD': 400, 'CM': 900}
        value_map = dict(roman_int_map, **new_char_map)
        total_map_list = sorted(value_map.items(), key=lambda x: x[1], reverse=True)
        result = ''
        while(num > 0):
            for entry in total_map_list:
                if num >= entry[1] and num % entry[1] >= 0:
                    # print(num, entry[0], entry[1])
                    result = result + entry[0]
                    num = num - entry[1]
                    break
        return result
        
tc = Solution().intToRoman(1994)
assert tc == "MCMXCIV", '{}==MCMXCIV'.format(tc)

tc = Solution().intToRoman(3)
assert tc == "III", '{}==III'.format(tc)

tc = Solution().intToRoman(20)
assert tc == "XX", '{}==XX'.format(tc)