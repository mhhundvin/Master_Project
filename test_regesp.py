import re

# def useRegex(input):
#     pattern = re.compile(r"#.*[a-zA-Z]", re.IGNORECASE)
#     return pattern.fullmatch(input)

# # match = useRegex("#comment")
# # if match:
# #     print(match.group(0))

# m = re.search('//(?=\[)', '//[^\n]*')
# if m:
#     print(m.group(0))

# m = re.search('(?<!=-)\w+', '-spam-egg')
# if m:
#     print(m.group(0))


txt = ""
with open("text.txt", 'r') as f:
    for line in f.readlines():
        txt += line
# re.purge()
p = re.compile('((\d+\.\d*|\.\d+)(e[-+]?\d+)?|\d+(e[-+]?\d+))')        #'0x[\da-f]0*')
m = p.findall(txt)

# m = re.search('0x[\da-f]0*',txt)
if m:
    print(f'-->{m}')