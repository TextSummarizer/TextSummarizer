# coding=utf-8
class _UtfCharMap:
    def __init__(self):
        self._char_map = {
            "\xc3\xa0": "a",
            "\xc3\xa8": "e",
            "\xc3\xac": "i",
            "\xc3\xb2": "o",
            "\xc3\xb9": "u"
        }
        self._char_list = ['\xc3', '\xa0', '\xa8', '\xac', '\xb2', '\xb9']

    def char_mapping(self, letter):
        try:
            return self._char_map[letter]
        except KeyError:
            return letter

    def is_strange_char(self, letter):
        if letter in self._char_list:
            return True
        else:
            return False


# I caratteri accentati vengono interpretati come due caratteri differenti. Questo metodi ne fa il merge
def _fix_token(source_token):
    destination_token_splitted = []
    letter_list = [y for y in source_token]
    n = len(letter_list)
    idx = 0

    while idx < n:
        letter = letter_list[idx]

        if utf_map.is_strange_char(letter):
            if idx < n:
                next_letter = letter_list[idx + 1]
                if utf_map.is_strange_char(next_letter):
                    letter_list[idx] = letter + next_letter
                    del letter_list[idx + 1]
                    n = n - 1

        destination_token_splitted.append(letter_list[idx])
        idx = idx + 1
    return destination_token_splitted


# Preso un token, vede i caratteri accentati che ci sono e li sostituisce con i non accentati
def smooth(input_token):
    fixed_splitted_token = _fix_token(input_token)
    strange_char_mapping = [utf_map.char_mapping(letter) for letter in fixed_splitted_token]
    return "".join(strange_char_mapping)


# Istanzio un utf map che verrà utilizzato dai metodi implementati sopra
utf_map = _UtfCharMap()

