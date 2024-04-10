import string

# Vigenere Solver
# https://en.wikipedia.org/wiki/Letter_frequency

# authors: Henrique Xavier e Lucas Antunes

# portuguese: 1,94 (0,074)
# english: 1,73 (0,066)
# random: 1,00 (0,0385)

alphabet = list(string.ascii_lowercase)

english = {
    'a': 8.167,
    'b': 1.492,
    'c': 2.782,
    'd': 4.253,
    'e': 12.702,
    'f': 2.228,
    'g': 2.015,
    'h': 6.094,
    'i': 6.966,
    'j': 0.253,
    'k': 1.772,
    'l': 4.025,
    'm': 2.406,
    'n': 6.749,
    'o': 7.507,
    'p': 1.929,
    'q': 0.095,
    'r': 5.987,
    's': 6.327,
    't': 9.056,
    'u': 2.758,
    'v': 0.978,
    'w': 2.360,
    'x': 0.250,
    'y': 1.974,
    'z': 0.07
}

portuguese = {
    'a': 14.63,
    'b': 1.04,
    'c': 3.88,
    'd': 4.99,
    'e': 12.57,
    'f': 1.02,
    'g': 1.30,
    'h': 1.28,
    'i': 6.18,
    'j': 0.40,
    'k': 0.02,
    'l': 2.78,
    'm': 4.74,
    'n': 5.05,
    'o': 10.73,
    'p': 2.52,
    'q': 1.20,
    'r': 6.53,
    's': 7.81,
    't': 4.34,
    'u': 4.63,
    'v': 1.67,
    'w': 0.01,
    'x': 0.21,
    'y': 0.01,
    'z': 0.47
}


def read_file(number):
    with open(f'ciphers/cipher{number}.txt', 'r') as file:
        return file.read()


def write_file(number, text):
    with open(f'decipher{number}.txt', 'w') as file:
        file.truncate()
        file.write(text)


# split text by into groups according to size
# exp: text = abcdef, size = 3, result = [[ad], [be], [cf]]
def split_text(text, size):
    groups = [[] for _ in range(size)]

    for pos, letter in enumerate(text):
        groups[pos % size].append(letter)

    return groups


def join_groups(groups):
    text = ''

    for col in range(len(groups[0])):
        for row in range(len(groups)):
            try:
                text += groups[row][col]
            except:
                continue

    return text


def calculate_coincidence_index(group):
    frequency = {letter: group.count(letter) for letter in set(group)}

    n = len(group)
    coincidence_index = sum(value * (value - 1) for value in frequency.values()) / (n * (n - 1))

    return coincidence_index


def estimate_key_size(number, _range=16):
    text = read_file(number)

    for size in range(1, _range + 1):
        groups = split_text(text, size)

        avg_coincidence_index = 0
        for group in groups:
            avg_coincidence_index += calculate_coincidence_index(group)

        avg_coincidence_index /= len(groups)

        if avg_coincidence_index > 0.07:
            return size


def calculate_frequencies(group):    
    return [(letter, round(100 * group.count(letter) / len(group), 4)) for letter in alphabet]


def calculate_score(shift, lang):
    score = 0
    for pos in range(len(alphabet)):
        _, frequency = shift[pos]
        score += frequency * lang[alphabet[pos]]

    return score


def estimate_key_letter(group, lang):
    frequencies = calculate_frequencies(group)
    best_shift = 0
    best_score = 0

    for shift in range(len(alphabet)):
        score = calculate_score(frequencies, lang)

        if score > best_score:
            best_score = score
            best_shift = shift
        
        frequencies.append(frequencies.pop(0))
    
    return chr(best_shift + 97)


def estimate_key(number, key_size, lang):
    text = read_file(number)
    groups = split_text(text, key_size)

    key = ''

    for group in groups:
        letter = estimate_key_letter(group, lang)
        key += letter

    return key


def vigenere_decipher(number, key):
    text = read_file(number)

    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    text_as_int = [ord(i) for i in text]
    plaintext = ''

    for i in range(len(text_as_int)):
        value = (text_as_int[i] - key_as_int[i % key_length]) % 26
        plaintext += chr(value + 97)

    write_file(case, plaintext)


if __name__ == '__main__':
    case = input('escolha um arquivo (1-31): ')
    print('-' * 20)
    print(f'case: {case}')

    key_size = estimate_key_size(case)
    print(f'key size: {key_size}')

    key = estimate_key(case, key_size, portuguese)
    print(f'key: {key}')

    vigenere_decipher(case, key)
