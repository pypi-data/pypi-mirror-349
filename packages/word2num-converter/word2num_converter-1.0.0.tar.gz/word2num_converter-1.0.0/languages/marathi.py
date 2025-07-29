import re

direct_dict = {'0': ['शून्य'],'1': ['एक'],'2': ['दोन'],'3': ['तीन'],'4': ['चार'],'5': ['पाच'],'6': ['सहा'],'7': ['सात'],'8': ['आठ'],'9': ['नऊ'],'10': ['दहा'],'11': ['अकरा'],'12': ['बारा'],'13': ['तेरा'],'14': ['चौदा'],'15': ['पंधरा'],'16': ['सोळा'],'17': ['सतरा'],'18': ['अठरा'],'19': ['एकोणीस'],'20': ['वीस'],'21': ['एकवीस'],'22': ['बावीस'],'23': ['तेवीस'],'24': ['चोवीस'],'25': ['पंचवीस'],'26': ['सव्वीस'],'27': ['सत्तावीस'],'28': ['अठ्ठावीस'],'29': ['एकोणतीस'],'30': ['तीस'],'31': ['एकतीस'],'32': ['बत्तीस'],'33': ['तेहेतीस'],'34': ['चौतीस'],'35': ['पस्तीस'],'36': ['छत्तीस'],'37': ['सदतीस'],'38': ['अडतीस'],'39': ['एकोणचाळीस'],'40': ['चाळीस'],'41': ['एक्केचाळीस'],'42': ['बेचाळीस'],'43': ['त्रेचाळीस'],'44': ['चव्वेचाळीस'],'45': ['पंचेचाळीस'],'46': ['सेहेचाळीस'],'47': ['सत्तेचाळीस'],'48': ['अठ्ठेचाळीस'],'49': ['एकोणपन्नास'],'50': ['पन्नास'],'51': ['एक्कावन्न'],'52': ['बावन्न'],'53': ['त्रेपन्न'],'54': ['चौपन्न'],'55': ['पंचावन्न'],'56': ['छप्पन्न'],'57': ['सत्तावन्न'],'58': ['अठ्ठावन्न'],'59': ['एकोणसाठ'],'60': ['साठ'],'61': ['एकसष्ट'],'62': ['बासष्ट'],'63': ['त्रेसष्ट'],'64': ['चौसष्ट'],'65': ['पासष्ट'],'66': ['सहासष्ट'],'67': ['सदुसष्ट'],'68': ['अडुसष्ट'],'69': ['एकोणसत्तर'],'70': ['सत्तर'],'71': ['एकाहत्तर'],'72': ['बाहत्तर'],'73': ['त्र्याहत्तर'],'74': ['चौर्‍याहत्तर'],'75': ['पंचाहत्तर'],'76': ['शाहत्तर'],'77': ['सत्त्याहत्तर'],'78': ['अठ्ठ्याहत्तर'],'79': ['एकोणऐंशी'],'80': ['ऐंशी'],'81': ['एक्याऐंशी'],'82': ['ब्याऐंशी'],'83': ['त्र्याऐंशी'],'84': ['चौऱ्याऐंशी'],'85': ['पंचाऐंशी'],'86': ['शहाऐंशी'],'87': ['सत्त्याऐंशी'],'88': ['अठ्ठ्याऐंशी'],'89': ['एकोणनव्वद'],'90': ['नव्वद'],'91': ['एक्याण्णव'],'92': ['ब्याण्णव'],'93': ['त्र्याण्णव'],'94': ['चौऱ्याण्णव'],'95': ['पंचाण्णव'],'96': ['शहाण्णव'],'97': ['सत्त्याण्णव'],'98': ['अठ्ठ्याण्णव'],'99': ['नव्याण्णव'],'100': ['शंभर'],'1000': ['हजार'],'100000': ['लाख'],'10000000': ['कोटी']}

higher_dict = {2 : ['शे'],3 : ['हज़ार'],5 : ['लाख'],7 : ['कोटी']}

exceptions_dict = {'0' : ['शून्य'],'100' : ['शंभर', 'एकशे']}

variations_dict = {'125' : ['सव्वाशे'],'150' : ['दीडशे'],'175' : ['पावणे दोनशे'],'225' : ['सव्वा दोनशे'],'250' : ['अडीचशे'],'275' : ['पावणे तीनशे'],'325' : ['सव्वा तीनशे'],'350' : ['साडे तीनशे'],'375' : ['पावणे चारशे'],'425' : ['सव्वा चारशे'],'450' : ['साडे चारशे'],'475' : ['पावणे पाचशे'],'525' : ['सव्वा पाचशे'],'550' : ['साडे पाचशे'], '575' : ['पावणे सहाशे'],'625' : ['सव्वा सहाशे'],'650' : ['साडे सहाशे'],'675' : ['पावणे सातशे'],'725' : ['सव्वा सातशे'],'750' : ['साडे सातशे'],'775' : ['पावणे आठशे'],'825' : ['सव्वा आठशे'],'850' : ['साडे आठशे'],'875' : ['पावणे नऊशे'],'925' : ['सव्वा नऊशे'],'950' : ['साडे नऊशे'],'975' : ['पावणे दहाशे']}

# Build reverse map
def build_dict(*dicts):
    reverse = {}
    for d in dicts:
        for number, phrases in d.items():
            for phrase in phrases:
                reverse[phrase.strip()] = int(number)
    return reverse

word_map = build_dict(direct_dict, exceptions_dict, variations_dict)
scale_keywords = {'कोटी': 10**7, 'लाख': 10**5, 'हजार': 10**3, 'शे': 100}

for scale_word, multiplier in scale_keywords.items():
    word_map[scale_word] = multiplier

known_phrases = sorted(word_map.keys(), key=len, reverse=True)
all_number_words = set(w for phrase in known_phrases for w in phrase.split())

# Handle Devanagari digits
def devnagari_to_eng_digit(word):
    return word.translate(str.maketrans("०१२३४५६७८९", "0123456789"))

def is_digit(word):
    try:
        int(devnagari_to_eng_digit(word))
        return True
    except:
        return False

def get_digit_value(word):
    return int(devnagari_to_eng_digit(word))

# Main phrase parser
def parse_indian_number_phrase(text):
    text = text.strip()
    tokens = []

    while text:
        matched = False
        for phrase in known_phrases:
            if text.startswith(phrase):
                tokens.append(phrase)
                text = text[len(phrase):].lstrip()
                matched = True
                break
        if not matched:
            digit_match = re.match(r'^([०१२३४५६७८९0-9]+)', text)
            if digit_match:
                digit_str = digit_match.group(1)
                tokens.append(digit_str)
                text = text[len(digit_str):].lstrip()
                matched = True
            else:
                raise ValueError(f"Unknown prefix in: {text}")

    # Group and calculate
    total = 0
    group_value = 0
    multipliers = {'कोटी': 10**7, 'लाख': 10**5, 'हजार': 10**3}

    for word in tokens:
        if is_digit(word):
            group_value += get_digit_value(word)
        elif word in multipliers:
            total += group_value * multipliers[word]
            group_value = 0
        elif word == 'शे':
            if group_value == 0:
                group_value = 1
            group_value *= 100
        elif word in word_map:
            group_value += word_map[word]
        else:
            raise ValueError(f"Unknown token: {word}")
    total += group_value
    return total

# FIXED: Better sentence parser
def convert_mar_number_phrases_in_sentence(sentence):
    words = sentence.strip().split()
    new_sentence = []
    i = 0

    def is_number_word(w):
        return is_digit(w) or w in word_map or w in scale_keywords or w in all_number_words

    while i < len(words):
        if is_number_word(words[i]):
            chunk = []
            while i < len(words) and is_number_word(words[i]):
                chunk.append(words[i])
                i += 1
            try:
                # Join chunk as string and parse
                val = parse_indian_number_phrase(' '.join(chunk))
                new_sentence.append(str(val))
            except Exception:
                new_sentence.extend(chunk)  # fallback
        else:
            new_sentence.append(words[i])
            i += 1

    return ' '.join(new_sentence)
