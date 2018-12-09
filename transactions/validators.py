def validate_tax_id(nip_str):
    """ check tax id """
    
    if '-' in nip_str:
        nip_str = nip_str.replace('-', '')
    if len(nip_str) != 10 or not nip_str.isdigit():
        return False
    digits = [int(i) for i in nip_str]
    weights = (6, 5, 7, 2, 3, 4, 5, 6, 7)
    check_sum = sum(d * w for d, w in zip(digits, weights)) % 11
    return check_sum == digits[9]


def validate_iban(num):
    """ check bank account number """
    
    COUNTRY_CODE = '2521'  # for Poland
    EXPECTED_LENGTH = 26

    if len(num) != EXPECTED_LENGTH:
        return False, 'Nieprawidłowa długość cyfr'
    
    i = int(''.join(num[2:] + COUNTRY_CODE + num[:2]))
    if i % 97 != 1:
        return False, 'Nieprawidłowa suma kontrolna.'
    return True, None
