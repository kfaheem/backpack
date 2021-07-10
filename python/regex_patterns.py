import regex
import inspect

text = """
Borrower Name is Arya Stark, 
daughter of Eddard Stark.
"""

pattern = regex.compile("\s*Borrower\s+Name\s+is\s+(?<self>\w+\s+\w+),\s+daughter\s+of\s+(?<parent>\w+\s+\w+)\.\s*",
                        regex.MULTILINE | regex.IGNORECASE)

print(regex.findall(pattern, text))

iter_obj = regex.finditer(pattern, text)

iter_obj_search = regex.search(pattern, text)
iter_obj_match = regex.match(pattern, text)
# print(list(iter_obj))
# print(iter_obj_search)
# print(iter_obj_match)

# print(iter_obj_search.group(2))
# print(iter_obj_match.span(2))

for m in regex.finditer(pattern, text):
    print(m.span())

for n in iter_obj:
    print(n.groupdict())
    print(n.span(1))
    print(n.start(1), n.end(1))


for n in regex.search(pattern, text):
    print(n.groupdict())
    print(n.span(1))
    print(n.start(1), n.end(1))
