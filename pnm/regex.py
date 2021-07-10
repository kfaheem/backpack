import regex
import nltk

pattern = regex.compile("(?e)some_text\w+\d*?(capture_group|another_group){e<=1}", regex.IGNORECASE |
                        regex.MULTILINE | regex.DOTALL)

# Checkout regexr.com for writing regex patterns

# regex.search or regex.finditer returns spans and capture group info
# .span() would return full span of pattern match
# .span(1) would return span of first capture group
# .start(1) .end(2) would return starting index of first capture group and ending index of second capture group
# .groups() similar to findall
# .group(1) returns actual text captured by first group
# .group_dict() returns actual text captured by groups in the form of a dict {"group_name" : "text"}
# for .group_dict() to work, capture group must be like (?<group_name>blah_blah)
# regex.findall returns actual text captured by groups in the form of a list


# Fuzzy matching
# ?e represents fuzzy matching
# {e<=1} matches with errors less than or eq to 1 will be returned
# other params available too - s, ... (Checkout documentation on regex for fuzzy matching)


# Lazy evaluation
# Adding a ? after a quantifier makes the pattern lazy, for ex *?

# forward looking
# If a group begins with ?= then the pattern before the group is matched, for ex - "match_this(?=capture_group)"


# distance matching - nltk

