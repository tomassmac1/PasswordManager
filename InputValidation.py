# Input validation for the whole program
# Validation follows relevant OWASP guidelines.


def initialise(user_input, input_type, check_len, low, high, check_bits):

    user_input = str()
    valid = True
    check_len = bool()
    check_bits = bool()
    encode_check(user_input, valid)
    type_check(user_input, valid, check_bits)
    length_check(check_len, valid, user_input, low, high)
    char_check(user_input, valid)
    return valid


def encode_check(user_input, valid):

    if isinstance(user_input, str):
        valid = True
    else:
        valid = False
    return valid


def type_check(user_input, valid, check_bits):
    if type(user_input) != str:
        valid = False
    if check_bits == True:
        if len(user_input) > 100:
            valid = False
    return valid


def length_check(check_len, valid, user_input, low, high):
    if check_len == True:
        try:
            new_user_input = int(user_input)
            if new_user_input < low:
                if new_user_input > high:
                    valid = False
        except ValueError:
            valid = False
    return valid


def char_check(user_input, valid):
    for _ in user_input:
        if _ in 'qwertyuiopasdfghjklzxcvbnm1234567890-=!£$^*_+[],.?':
            valid = True
        else:
            valid = False
    return valid



