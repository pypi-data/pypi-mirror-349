import re

# Word to number
word_to_num = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13,'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17,'eighteen': 18, 'nineteen': 19, 'twenty': 20, 'thirty': 30,'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70,'eighty': 80, 'ninety': 90}

# Multipliers
multipliers = {'hundred': 100,'thousand': 1000,'lakh': 100000,'crore': 10000000}

def token_to_number(token):
    if token.isdigit():
        return int(token)
    elif token in word_to_num:
        return word_to_num[token]
    return None

def words_to_number(tokens):
    total = 0
    current = 0
    for token in tokens:
        if token == 'and':
            continue
        elif token in multipliers:
            if current == 0:
                current = 1
            current *= multipliers[token]
            total += current
            current = 0
        else:
            value = token_to_number(token)
            if value is None:
                return None
            current += value
    total += current
    return total

def convert_eng_number_phrases_in_sentence(sentence):
    original_words = sentence.split()
    lower_words = [w.lower() for w in original_words]
    result = []
    i = 0

    while i < len(lower_words):
        matched = False
        max_j = i
        max_val = None

        for j in range(i+1, len(lower_words)+1):
            chunk = lower_words[i:j]
            val = words_to_number(chunk)
            if val is not None:
                max_j = j
                max_val = val

        if max_val is not None:
            result.append(str(max_val))
            i = max_j
        else:
            result.append(original_words[i])
            i += 1

    return ' '.join(result)