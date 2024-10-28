text = "0001003001000"
pattern = "001000"

def construct_prefix_table(pattern):
    """
        Responsable to construct the prefix table. The concept is:
        For each prefix of the pattern, we have to find the longest
        suffix that is also a prefix of the pattern. For example:
            * pattern = "abac"
            * prefix_table = [0, 0, 1, 0]
        The first element is always 0, because there is no prefix
        before the first element. The second element is also 0, because
        there is no prefix before the second element. The third element
        is 1, because the longest suffix that is also a prefix is "a".
        The fourth element is 0, because there is no prefix before the
        fourth element.
    """

    pattern = "%" + pattern

    prefix_table = [0] * len(pattern)
    k = 0

    for q in range(2, len(pattern)):
        while pattern[k+1] != pattern[q] and k > 0:
            k = prefix_table[k]

        if pattern[k+1] == pattern[q]:
            k += 1

        prefix_table[q] = k
    
    return prefix_table

def kmp(text, pattern, prefix_table):
    """
        This function is responsable to find the pattern in the text, using
        the KMP algorithm.
    """
    text = "%" + text
    pattern = "%" + pattern

    l = 0
    for s in range(1, len(text)):
        while l > 0 and pattern[l + 1] != text[s]:
            l = prefix_table[l]
        
        if pattern[l + 1] == text[s]:
            l = l + 1
        
        if l == len(pattern)-1:
            print(f"Occours on {s-len(pattern)+1}")
            l = prefix_table[l]


if __name__ == "__main__":
    table = construct_prefix_table(pattern)

    kmp(text, pattern, table)