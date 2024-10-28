text = ""
pattern = "the quick brown fox jumped over a lazy cat"
alphabet = list(set(pattern))

def construct_shift_table(pattern, alphabet):
    """
        This function is responsable to construct the shift table. The concept is:
        For each character in the alphabet, we have to find the shift that we have
        to do in the pattern to align the character with the last character of the
        pattern. For example:
            * pattern = "BARBER"
            * alphabet = ['A', 'B', 'E', 'R']
            * shift_table = {'A': 4, 'B': 2, 'E': 1, 'R': 3}
        The character 'A' has to be shifted 6 positions to align with the last character
        of the pattern. The character 'B' has to be shifted 5 positions to align with the
        last character of the pattern. The character 'E' has to be shifted 6 positions to
        align with the last character of the pattern. The character 'R' has to be shifted
        1 position to align with the last character of the pattern.
    """
    table = {}
    
    for c in alphabet:
        table[c] = len(pattern)

    for k in range(len(pattern)-1):
        table[pattern[k]] = len(pattern) - 1 - k

    return table


def horspool(text, pattern, table):
    """
        This function is responsable to find the pattern in the text, using
        the Horspool algorithm.
    """
    m = len(pattern)
    n = len(text)
    i = m - 1

    while i < n:
        k = 0
        while k < m and pattern[m - 1 - k] == text[i - k]:
            k += 1
        
        if k == m:
            print(f"Occours on {i - m + 1}")
            return True
        else:
            i += table[text[i]]

    return False

if __name__ == "__main__":
    table = construct_shift_table(pattern, alphabet)
    print(table)

    # print(horspool(text, pattern, table))