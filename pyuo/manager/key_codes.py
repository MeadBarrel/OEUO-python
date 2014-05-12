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
    'SHIFT': 0x10,
    'CONTROL': 0x11,
    'ALT': 0x12,
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
    'DEL': 0x2e
}

numeric_codes = {str(i): 0x30+i for i in xrange(10)}
letter_codes = {c: 0x41+i for (i, c) in enumerate(ascii_lowercase)}

codes = local_codes
codes.update(numeric_codes)
codes.update(letter_codes)
