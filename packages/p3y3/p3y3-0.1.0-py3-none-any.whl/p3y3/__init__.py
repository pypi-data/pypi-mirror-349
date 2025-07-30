"""
3y3 encoding in python - see https://synthetic.garden/3y3.htm
This lets you hide text in plain sight.
It's a Hypnospace Outlaw reference!
https://store.steampowered.com/app/844590/Hypnospace_Outlaw/
"""


def decode(text: str) -> str:
    """
    Decode 3y3 (invisible) text.
    Equivalent to:
    ```
    def decode(text: str) -> str:
    ret = ''
    for char in text:
        i = ord(char)
        i = i - 0xe0000 if 0xe0000 < i < 0xe007f else 0
        ret += chr(i)
    return ret
    ```
    """

    return ''.join((chr(i - 0xe0000 if 0xe0000 < i < 0xe007f else i) for i in map(ord, text)))


def encode(text: str) -> str:
    """
    Encode text in 3y3 (invisible text).
    Equivalent to:
    ```
    def encode(text: str) -> str:
    ret = ''
    for char in text:
        i = ord(char)
        i = i + 0xe0000 if 0x00 < i < 0x7f else 0
        ret += chr(i)
    return ret
    ```
    """

    return ''.join((chr(i + 0xe0000 if 0x00 < i < 0x7f else i) for i in map(ord, text)))


def second_sightify(text: str) -> str:
    """
    Try to decode 3y3, otherwise encode it.
    https://hypnospace.wiki.gg/wiki/Second_Sight
    """
    if any(map(lambda c: 0xe0000 < ord(c) < 0xe007f, text)):
        return decode(text)
    else:
        return encode(text)


if __name__ == "__main__":
    print(repr(second_sightify("Hello, world!")))
