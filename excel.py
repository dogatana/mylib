def a_to_c(str):
    """conver column string notation(A1) to column number(1..)

    >>> a_to_c('A')
    1
    >>> a_to_c('z')
    26
    >>> a_to_c('Aa')
    27
    >>> a_to_c('XfD')
    16384
    >>> a_to_c('?')  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError
    >>> a_to_c('XFE')  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError
    """
    col = 0
    for c in str.upper():
        if c < "A" or c > "Z":
            raise ValueError("invalid character")
        col = col * 26 + ord(c) - ord("@")
    if col > 16384:
        raise ValueError("out of range")
    return col


def c_to_a(col):
    """conver column number(1..) to string notation(A1)

    >>> c_to_a(1)
    'A'
    >>> c_to_a(26)
    'Z'
    >>> c_to_a(27)
    'AA'
    >>> c_to_a(16384)
    'XFD'
    >>> c_to_a(0)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError
    >>> c_to_a(16385)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError
    """
    if col < 1 or col > a_to_c("XFD"):
        raise ValueError("out of range")
    str = ""
    while col > 26:
        col, r = divmod(col, 26)
        str = chr(r + 64) + str
    str = chr(col + 64) + str
    return str


def rc_to_a1(y, x):
    """return A1 string from (y, x)

    >>> rc_to_a1(1, 1)
    'A1'
    >>> rc_to_a1(2, 2)
    'B2'
    >>> rc_to_a1(1, 16384)
    'XFD1'
    >>> rc_to_a1(0, 1)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError
    >>> rc_to_a1(1, 0)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError
    >>> rc_to_a1(1, 16385)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError
    """
    if y < 1 or x < 1 or x > 16384:
        raise ValueError("out of range")
    return c_to_a(x) + str(y)


def a1_to_rc(str):
    """retrun tuple (y, x) form a1 str

    >>> a1_to_rc('A1')
    (1, 1)
    >>> a1_to_rc('B2')
    (2, 2)
    >>> a1_to_rc('  XFD123  ')
    (123, 16384)
    >>> a1_to_rc('A0')  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError
    >>> a1_to_rc('#1')  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError
    >>> a1_to_rc('XFE1')  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError
    """
    import re

    m = re.match(r"^(?P<col>[a-zA-Z]+)(?P<row>\d+)$", str.strip())
    if not m:
        raise ValueError("invalid argument")
    row = int(m.group("row"))
    if row < 1:
        raise ValueError("invalid argument")
    return row, a_to_c(m.group("col"))


def windows_path(path):
    return path.replace("/", "\\")


def RGB(red, green, blue):
    """calcurate one color value from red, green, blue

    >>> RGB(0, 0, 0)
    0
    >>> '%06x' % RGB(255, 0, 0)
    'ff0000'
    >>> '%06x' % RGB(0, 255, 0)
    '00ff00'
    >>> '%06x' % RGB(0, 0, 255)
    '0000ff'
    >>> '%06x' % RGB(257, 258, 259)
    '010203'
    """
    return ((red & 0xFF) * 256 + (green & 0xFF)) * 256 + (blue & 0xFF)


def excel(visible=True):
    "return Excel OLE Ojbect"

    import win32com.client

    app = win32com.client.Dispatch("Excel.Application")
    app.Visible = visible
    return app


if __name__ == "__main__":
    import doctest

    doctest.testmod()
