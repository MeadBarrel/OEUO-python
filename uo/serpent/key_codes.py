from string import ascii_lowercase

local_codes = {
    'LBUTTON': 0x01,
     'RBUTTON': 0x02,
    'CANCEL': 0x03,
    'MBUTTON': 0x04,
    'X1BUTTON': 0x05,
    'X2Button': 0x06,
    'BACK': 0x08,
    'TAB': 0x09,
    'CLEAR': 0x0c,
    'RETURN': 0x0d,
    'PAUSE': 0x13,
    'CAPS': 0x14,
    'SPACE': 0x20,
    'PGUP': 0x21,
    'PGDN': 0x22,
    'END': 0x23,
    'HOME': 0x24,
    'LEFT': 0x25,
    'UP': 0x26,
    'RIGHT': 0x27,
    'DOWN': 0x28,
    'SELECT': 0x29,
    'PRINT': 0x30,
    'PRTSCRN': 0x2c,
    'INS': 0x2d,
    'DEL': 0x2e,
    'LWIN': 0x5b,
    'RWIN': 0x5c,
    'APPS': 0x5d,
    'NP0': 0x60,
    'NP1': 0x61,
    'NP2': 0x62,
    'NP3': 0x63,
    'NP4': 0x64,
    'NP5': 0x65,
    'NP6': 0x66,
    'NP7': 0x67,
    'NP8': 0x68,
    'NP9': 0x69,
    'MULTIPLY': 0x6a,
    'ADD': 0x6b,
    'SEP': 0x6c,
    'SUB': 0x6d,
    'DEC': 0x6e,
    'DIV': 0x6f,
    'NUMLOCK': 0x90,
    'SCROLL': 0x91,
    'LSHIFT': 0xa0,
    'RSHIFT': 0xa1,
    'LCONTROL': 0xa2,
    'RCONTROL': 0xa3,
    'LMENU': 0xa4,
    'RMENU': 0xa5,
}

f_codes = {str(i): 0x70+i for i in xrange(25)}
numeric_codes = {str(i): 0x30+i for i in xrange(10)}
letter_codes = {c: 0x41+i for (i, c) in enumerate(ascii_lowercase)}


codes = local_codes
codes.update(numeric_codes)
codes.update(letter_codes)
codes.update(f_codes)