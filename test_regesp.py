import re

def useRegex(input):
    pattern = re.compile(r"#.*[a-zA-Z]", re.IGNORECASE)
    return pattern.fullmatch(input)

# match = useRegex("#comment")
# if match:
#     print(match.group(0))

m = re.search('//(?=\[)', '//[^\n]*')
if m:
    print(m.group(0))

m = re.search('(?<!=-)\w+', '-spam-egg')
if m:
    print(m.group(0))