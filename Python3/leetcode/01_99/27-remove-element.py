class Solution:
    def removeElement(self, nums, val):
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """
        i = 0
        j = 0
        for j in range(len(nums)):
            if nums[j] != val:
                nums[i] = nums[j]
                i = i + 1
        return i


assert Solution().removeElement([0,1,2,2,3,0,4,2], 2) == 5, '{}==5'.format(Solution().removeElement([0,1,2,2,3,0,4,2], 2))
assert Solution().removeElement([0, 1, 2, 2, 3, 0, 4, 2], 2) == 5, '{}==2'.format(Solution().removeElement([], 2))
assert Solution().removeElement([3,2,2,3], 2) == 2, '{}==2'.format(Solution().removeElement([], 2))