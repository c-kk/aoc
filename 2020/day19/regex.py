import re

# Regex tutorial

#
# Metacharacters have special meaning
#

# . ^ $ * + ? { } [ ] \ | ( )

# [ ] = specifying a character class
# [abc] will match any of the characters a, b, or c. This is the same as [a-c]
# Metacharacters are not active inside classes: [akm$]
# [^5] will match any character except '5'

# \ Can start a special sequence or escape an character
# \d Matches any decimal digit; this is equivalent to the class [0-9]
# \D Matches any non-digit character; this is equivalent to the class [^0-9]
# \s Matches any whitespace character; this is equivalent to the class [ \t\n\r\f\v]
# \S Matches any non-whitespace character; this is equivalent to the class [^ \t\n\r\f\v]
# \w Matches any alphanumeric character; this is equivalent to the class [a-zA-Z0-9_]
# \W Matches any non-alphanumeric character; this is equivalent to the class [^a-zA-Z0-9_]

# Special sequences can be included in a class
# [\s,.] will match any whitespace character, or ',' or '.'

# . It matches anything except a newline character. It is often used where you want to match “any character”.

# Repeating things: * +
# Repetitions are greedy
# * the previous character can be matched zero or more times, instead of exactly once. ca*t will match 'ct', 'cat', 'caaat', and so forth. 
# + the previous character can be matched one or more times, instead of exactly once
# ? matches either once or zero times. Think about it as 'optional': home-?brew matches either 'homebrew' or 'home-brew'.
# {m,n} there must be at least m (default 0) repetitions, and at most n (default unlimited). a/{1,3}b will match 'a/b', 'a//b', and 'a///b'. It won’t match 'ab', which has no slashes, or 'a////b', which has four.
# *?, +?, ??, or {m,n}? are non-greedy qualifiers which match as little text as possible.

# Step-by-step example
# RE = a[bcd]*b   string = 'abcbd'
#
# Step 1. a - matched
# Step 2. abcbd - The engine matches [bcd]*, going as far as it can, which is to the end of the string.
# Step 3. Failure - The engine tries to match b, but the current position is at the end of the string, so it fails.
# Step 4. abcb - Back up, so that [bcd]* matches one less character.
# Step 5. Failure - Try b again, but the current position is at the last character, which is a 'd'.
# Step 6. abc - Back up again, so that [bcd]* is only matching bc.
# Step 7. abcb - Try b again. This time the character at the current position is 'b', so it succeeds.
#
# Match = abcb

# Zero-width assertions (don't repeat those)
# |  the “or” operator. A|B will match any string that matches either A or B.
# ^  Matches at the beginning of lines. Unless the MULTILINE flag has been set, this will only match at the beginning of the string.
#    print(re.search('^From', 'From Here to Eternity')) 
# $  Matches at the end of a line, which is defined as either the end of the string, or any location followed by a newline character.
#    print(re.search('}$', '{block}\n'))
# \A Matches only at the start of the string. When not in MULTILINE mode, \A and ^ are effectively the same.
# \Z Matches only at the end of the string.
# \b Word boundary. This is a zero-width assertion that matches only at the beginning or end of a word.
#    p = re.compile(r'\bclass\b') print(p.search('no class at all'))
# \B Another zero-width assertion, this is the opposite of \b, only matching when the current position is not at a word boundary.

#
# Compiling Regular Expressions
#

# Regular expressions are compiled into pattern objects, 
# which have methods for various operations such as searching for pattern matches or performing string substitutions.
# p = re.compile('ab*')
# p = re.compile('ab*', re.IGNORECASE) also accepts an optional flags argument, used to enable various special features and syntax variations
# Compilation flags: ASCII, A, DOTALL, S, IGNORECASE, I, MULTILINE, M, VERBOSE, X (for ‘extended’)

# The Backslash Plague solution is to use raw strings
# "\\\\section" => r"\\section"
# "\\w+\\s+\\1" => r"\w+\s+\1"

# Verbose setting (re.VERBOSE)
# Whitespace is ignored, except when in character class or with unescaped backslash
# Also lets you put comments within a RE that will be ignored by the engine
#
# charref = re.compile(r"""
#  &[#]                # Start of a numeric entity reference
#  (
#      0[0-7]+         # Octal form
#    | [0-9]+          # Decimal form
#    | x[0-9a-fA-F]+   # Hexadecimal form
#  )
#  ;                   # Trailing semicolon
# """, re.VERBOSE)
#
# p = re.compile(r"""
#  \s*                 # Skip leading whitespace
#  (?P<header>[^:]+)   # Header name
#  \s* :               # Whitespace, and a colon
#  (?P<value>.*?)      # The header's value -- *? used to lose the following trailing whitespace
#  \s*$                # Trailing whitespace to end-of-line
# """, re.VERBOSE)

#
# Performing Matches
#

# match()     Determine if the RE matches at the beginning of the string.
# search()    Scan through a string, looking for any location where this RE matches.
# findall()   Find all substrings where the RE matches, and returns them as a list.
# finditer()  Find all substrings where the RE matches, and returns them as an iterator. 

# Example 1
# p = re.compile('[a-z]+')
#
# m = p.match('tempo') => <re.Match object; span=(0, 5), match='tempo'>
# m.group() => 'tempo'
# m.start(), m.end() => (0, 5)
# m.span() => (0, 5)
#
# m = r.search('::: message') => <re.Match object; span=(4, 11), match='message'>

# Example 2
# p = re.compile(r'\d+')
# p.findall('12 drummers drumming, 11 pipers piping, 10 lords a-leaping') => ['12', '11', '10']
#
# iterator = p.finditer('12 drummers drumming, 11 ... 10 ...')
# for match in iterator: print(match.span() => (0, 2) (22, 24) (29, 31)

# Module-Level Functions
# The re module also provides top-level functions called match(), search(), findall(), sub(), and so forth.
# re.match(r'From\s+', 'From amk Thu May 14 19:12:10 1998')  
# <re.Match object; span=(0, 5), match='From '>

#
# Grouping
# 

# Regular expressions are often used to dissect strings by writing a RE divided into several subgroups which match different components of interest. 
# Groups are marked by the '(', ')' metacharacters.
#
# p = re.compile('(ab)*'), print(p.match('ababababab').span()) => (0, 10)
#
# p = re.compile('(a(b)c)d')
# m = p.match('abcd')
# m.group(0) => 'abcd' Group 0 is always the complete match
# m.group(1) => 'abc'
# m.group(2) => 'b'
# m.group(2,1,2) => ('b', 'abc', 'b')
# m.groups() => ('abc', 'b')

# Backreferences in a pattern allow you to specify that the contents of an earlier capturing group must also be found at the current location in the string.
# For example, \1 will succeed if the exact contents of group 1 can be found at the current position, and fails otherwise.
# p = re.compile(r'\b(\w+)\s+\1\b') => \1 verwacht de inhoud van de vorige groep op die plek (\w+)
# p.search('Paris in the the spring').group()
# 'the the'

# Non-capturing groups
# Sometimes you’ll want to use a group to denote a part of a regular expression, but aren’t interested in retrieving the group’s contents.
# You can make this fact explicit by using a non-capturing group: (?:...), where you can replace the ... with any other regular expression.
# 
# m = re.match("([abc])+", "abc")
# m.groups() => ('c',)
# m = re.match("(?:[abc])+", "abc") # Ignoring the first group
# m.groups()

# Named groups
# Named groups behave exactly like capturing groups, and additionally associate a name with a group.
#
# p = re.compile(r'(?P<word>\b\w+\b)')
# m = p.search( '(((( Lots of punctuation )))' )
# m.group('word') => 'Lots'
# m.group(1) => 'Lots'
#
# Additionally, you can retrieve named groups as a dictionary with groupdict():
# m = re.match(r'(?P<first>\w+) (?P<last>\w+)', 'Jane Doe')
# m.groupdict() => {'first': 'Jane', 'last': 'Doe'}
#
# Example with a lot of named groups:
# InternalDate = re.compile(r'INTERNALDATE "'
#        r'(?P<day>[ 123][0-9])-(?P<mon>[A-Z][a-z][a-z])-'
#        r'(?P<year>[0-9][0-9][0-9][0-9])'
#        r' (?P<hour>[0-9][0-9]):(?P<min>[0-9][0-9]):(?P<sec>[0-9][0-9])'
#        r' (?P<zonen>[-+])(?P<zoneh>[0-9][0-9])(?P<zonem>[0-9][0-9])'
#        r'"')
#
# (?P=name) indicates that the contents of the group called name should again be matched at the current point.
# p = re.compile(r'\b(?P<word>\w+)\s+(?P=word)\b')
# p.search('Paris in the the spring').group() => 'the the'

#
# Lookahead Assertions 
#

# (?=...) Positive lookahead assertion. This succeeds if the contained regular expression, represented here by ..., successfully matches at the current location, and fails otherwise. But, once the contained expression has been tried, the matching engine doesn’t advance at all; the rest of the pattern is tried right where the assertion started.
# (?!...) Negative lookahead assertion. This is the opposite of the positive assertion; it succeeds if the contained expression doesn’t match at the current position in the string.
#
# Example: 
# Match a filename and split it apart into a base name and an extension, separated by a .
# .*[.].*$
# Exclude both bat and exe as extensions
# Don't: .*[.]([^b].?.?|.[^a]?.?|..?[^t]?)$
# Do:    .*[.](?!bat$|exe$)[^.]*$ 

#
# Modifying Strings
#

# split() Split the string into a list, splitting it wherever the RE matches
# sub()   Find all substrings where the RE matches, and replace them with a different string
# subn()  Does the same thing as sub(), but returns the new string and the number of replacements

# Split: .split(string[, maxsplit=0])
# p = re.compile(r'\W+')
# p.split('This is a test, short and sweet, of split().')    => ['This', 'is', 'a', 'test', 'short', 'and', 'sweet', 'of', 'split', '']
# p.split('This is a test, short and sweet, of split().', 3) => ['This', 'is', 'a', 'test, short and sweet, of split().']
#
# Keep delimiter
# p = re.compile(r'\W+')
# p.split('This... is a test.')  => ['This', 'is', 'a', 'test', '']
# p2 = re.compile(r'(\W+)')
# p2.split('This... is a test.') => ['This', '... ', 'is', ' ', 'a', ' ', 'test', '.', '']
#
# Module-level function
# re.split(r'[\W]+', 'Words, words, words.') => ['Words', 'words', 'words', '']

# Search and replace: .sub(replacement, string[, count=0])
# p = re.compile('(blue|white|red)')
# p.sub('colour', 'blue socks and red shoes') => 'colour socks and colour shoes'
#
# Use a function
# def hexrepl(match):
#     "Return the hex string for a decimal number"
#     value = int(match.group())
#     return hex(value)
#
# p = re.compile(r'\d+')
# p.sub(hexrepl, 'Call 65490 for printing, 49152 for user code.')

# Websites
# Source: https://docs.python.org/dev/howto/regex.html
# Other site: http://www.regular-expressions.info/index.html

