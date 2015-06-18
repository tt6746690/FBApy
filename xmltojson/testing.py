from bs4 import BeautifulSoup
soup = BeautifulSoup("<head><title id='wtf'><p>TEXT</p></title></head>")

soup2 = BeautifulSoup("<hello id='wtf'>wtf</hello>", "xml")

def test(tag):
    return tag.contents[0]

def is_the_only_string_within_a_tag(s):
    """Return True if this string is the only child of its parent tag."""
    return (s == s.parent.string)

# soup.find_all(text=is_the_only_string_within_a_tag)
print(soup2.hello.attrs)
print(soup.head.title.p.contents[0])
print(is_the_only_string_within_a_tag(soup2.hello.string))
print(test(soup2).contents)
print(soup2.find_all('hello', attrs=True))
print(soup2.find_all(text=None))