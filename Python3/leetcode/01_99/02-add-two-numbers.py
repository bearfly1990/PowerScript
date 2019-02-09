# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

    def set_next(self, x):
        self.next = x

    def __str__(self):
        current_node = self
        result = str(current_node.val)
        while (current_node.next):
            result = result + '->' + str(current_node.next.val)
            current_node = current_node.next
        return result

def create_listNode_list(org_list):
    if len(org_list) == 0:
        return
    new_list_node = ListNode(org_list[0])
    first_list_node = new_list_node

    for i in range(1, len(org_list)):
        new_list_node.set_next(ListNode(org_list[i]))
        new_list_node = new_list_node.next

    return first_list_node


class Solution:
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        carry = 0
        final_first_node = None
        current_node = None
        while (l1 or l2):
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0
            value = val1 + val2 + carry
            carry = value // 10
            value = value % 10
            if final_first_node is None:
                final_first_node = ListNode(value)
                current_node = final_first_node
            else:
                current_node.next = ListNode(value)
                current_node = current_node.next
            if l1: l1 = l1.next
            if l2: l2 = l2.next
            if carry:
                current_node.next = ListNode(1)
        return final_first_node

tc = Solution().addTwoNumbers(create_listNode_list([2, 4, 3]), create_listNode_list([5, 6, 4]))
print(tc)

tc = Solution().addTwoNumbers(create_listNode_list([2, 4, 3, 1]), create_listNode_list([5, 6, 4]))
print(tc)

tc = Solution().addTwoNumbers(create_listNode_list([2, 4, 5, 9,9,9]), create_listNode_list([5, 6, 4]))
print(tc)