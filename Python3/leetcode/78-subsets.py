class Solution:
    def subsets(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        subsets = [[]]
        for num in nums:
            copy_subsets = subsets.copy()
            for item in copy_subsets:
                print(num, item)
                subsets.append(item + [num])
                # subsets.append([num] + item)
        return subsets

tc = Solution().subsets([1,2,3])
# assert tc == ?, '{}==?'.format(tc)