import itertools

def generate_variants(word):
    return set([
        word,
        word.lower(), word.upper(), word.title(),
        word + '123', word + '2024', word + '2025',
        word[::-1],
        word.replace('a', '@').replace('s', '$').replace('i', '1').replace('e', '3')
    ])

def generate_wordlist(inputs):
    base_variants = set()
    for word in inputs:
        base_variants.update(generate_variants(word))
    for combo in itertools.permutations(inputs, 2):
        base_variants.add(''.join(combo))
    return list(base_variants)

def export_wordlist(wordlist, filename="wordlist.txt"):
    with open(filename, 'w') as f:
        for word in sorted(wordlist):
            f.write(f"{word}\n")
