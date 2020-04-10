def isVowel(c):

    return (c == 'a' or c == 'e' or c == 'i'
            or c == 'o' or c == 'u')


# Function to return the count of sub-strings
# that contain every vowel at least
# once and no consonant
def countSubstringsUtil(s):

    count = 0

    # Map is used to store count of each vowel
    mp = dict.fromkeys(s, 0)

    n = len(s)

    # Start index is set to 0 initially
    start = 0

    for i in range(n):
        mp[s[i]] += 1

        # If substring till now have all vowels
        # atleast once increment start index until
        # there are all vowels present between
        # (start, i) and add n - i each time
        while (mp['a'] > 0 and mp['e'] > 0
               and mp['i'] > 0 and mp['o'] > 0
               and mp['u'] > 0):
            count += n - i
            mp[s[start]] -= 1
            start += 1

    return count

# Function to extract all maximum length
# sub-strings in s that contain only vowels
# and then calls the countSubstringsUtil() to find
# the count of valid sub-strings in that string


def countSubstrings(s):

    count = 0
    temp = ""

    for i in range(len(s)):

        # If current character is a vowel then
        # append it to the temp string
        if (isVowel(s[i])):
            temp += s[i]

        # The sub-string containing all vowels ends here
        else:

            # If there was a valid sub-string
            if (len(temp) > 0):
                count += countSubstringsUtil(temp)

            # Reset temp string
            temp = ""

    # For the last valid sub-string
    if (len(temp) > 0):
        count += countSubstringsUtil(temp)

    return count


# Driver code
if __name__ == "__main__":

    s = "aeouisddaaeeiouua"

    print(countSubstrings(s))

# This code is contributed by AnkitRai01


def is_vowel(c):
    return c in 'aeiou'


# Function to return the count of sub-strings
# that contain every vowel at least
# once and no consonant
def count_substring_help(s):

    count = 0

    mp = dict.fromkeys(s, 0)

    n = len(s)

    start = 0

    for i in range(n):
        mp[s[i]] += 1

        while (mp['a'] > 0 and mp['e'] > 0
               and mp['i'] > 0 and mp['o'] > 0
               and mp['u'] > 0):
            count += n - i
            mp[s[start]] -= 1
            start += 1

    return count

# Function to extract all maximum length
# sub-strings in s that contain only vowels
# and then calls the countSubstringsUtil() to find
# the count of valid sub-strings in that string


def countSubstrings(s):

    count = 0
    temp = ""

    for i in range(len(s)):
        if (isVowel(s[i])):
            temp += s[i]

        else:
            if (len(temp) > 0):
                count += count_substring_help(temp)

            temp = ""

    if (len(temp) > 0):
        count += count_substring_help(temp)

    return count


def sequence_sum(a, n, d):
    return int((n*(2*a + (n-1) * d)) / 2)


def getSequenceSum(i, j, k):
    a_1 = i
    n_1 = abs(j - i + 1)
    d_1 = 1

    a_2 = j-1
    n_2 = abs(k - j)
    d_2 = -1

    return sequence_sum(a_1, n_1, d_1) + sequence_sum(a_2, n_2, d_2)

SELECT f.name FROM families f WHERE f.bill_id IN ()

SELECT b.id as bill_sum FROM bills b HAVING MAX(sum(b.amount)) GROUP BY b.id  ORDER BY bill_sum DESC





