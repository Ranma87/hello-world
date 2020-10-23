def compare(regex_, input_):
    """ Compares an input string of any length to a certain regex.
        Rules:
            an empty regex always returns True
            an empty input always returns False, except when regex is empty
            regex = '.' matches any input.
    """

    if len(regex_) == 0:
        return True

    if len(input_) == 0 and regex_ != '$':
        return False

    if len(input_) == 0 and regex_ == '$':
        return True

    if regex_[0] == '.' and not next_repeated(regex_):
        return compare(regex_[1:], input_[1:])

    if regex_[0] == '.' and next_repeated(regex_):
        # check when the next char in regex matches the input.
        next_char = wildcard_repeated(regex_, input_)
        if next_char == -1:
            return False
        if next_char == -2:
            return True
        return compare(regex_[2:], input_[next_char:])

    if regex_[0] in ('?', '+', '*'):
        return compare(regex_[1:], input_[:])

    # check if the next char should be treated as a literal
    if regex_[0] == '\\':
     #   print(regex_, 'antes.')
        regex_ = regex_[1:]
      #  print(regex_, 'luego.')

    if input_[0] == regex_[0] and not next_repeated(regex_):
        return compare(regex_[1:], input_[1:])

    if input_[0] == regex_[0] and next_repeated(regex_[:]):

        # check when the next char in regex matches the input.
        next_char = wildcard_repeated(regex_[:], input_)
        if next_char == -1:
            return False
        if next_char == -2:
            return True

        return compare(regex_[2:], input_[next_char:])

    if can_be_absent(regex_[:]):
        return compare(regex_[2:], input_[:])

    return False


def entry(main_regex, main_input):

    if not main_regex:
        return True

    if main_regex[0] == '^':
        return compare(main_regex[1:], main_input)

    for i in range(len(main_input)):
        if compare(main_regex, main_input[i:len(main_regex) + 1 + i]):
            return True

    return False


def next_repeated(rg):
    """checks if the next character, if exists, is * or +"""
    if len(rg) == 1:
        return False
    if rg[1] in ('*', '+'):
        return True

    return False


def can_be_absent(rg_):
    """checks if the next character, if exists, is * or ?"""
    if len(rg_) == 1:
        return False
    if rg_[1] in ('*', '?'):
        return True
    return False


def wildcard_repeated(w_regex, w_input):
    """ Returns the index of the input where the next character in the
    regex is matched. If no match returns -1.
    If no more characters in the regex, returns -2"""
    # w_regex[0:2) is always equal to .*
    if len(w_regex) > 2:
        for index, char in enumerate(w_input):
            if char == w_regex[2]:
                return index
        return -1
    return -2


if __name__ == '__main__':
    regex, input_str = input().split('|')
    print(entry(regex, input_str))
