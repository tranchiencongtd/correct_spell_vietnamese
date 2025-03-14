import random
import unidecode

def create_vietnamese_noise(text, noise_level=0.3):

    def abbreviation_error(word):
        abbreviations = {
            'không': 'ko', 'gì': 'j', 'được': 'dc', 'biết': 'bít',
            'làm': 'lm', 'vậy': 'vậ', 'thế': 'thế', 'người': 'ng',
            'chồng': 'ck', 'vợ': 'vk', 'yêu': 'iu', 'quá': 'qá'
        }
        return abbreviations.get(word.lower(), word)

    def swap_accent(char):
        accent_map = {
            'a': 'áàảãạâấầẩẫậăắằẳẵặ',
            'e': 'éèẻẽẹêếềểễệ',
            'i': 'íìỉĩị',
            'o': 'óòỏõọôốồổỗộơớờởỡợ',
            'u': 'úùủũụưứừửữự',
            'y': 'ýỳỷỹỵ'
        }
        for base, accents in accent_map.items():
            if char in accents:
                return random.choice(accents)
        return char

    def common_typo(char):
        typo_map = {
            'ch': 'tr', 'tr': 'ch',
            's': 'x', 'x': 's',
            'd': 'gi', 'gi': 'd',
            'l': 'n', 'n': 'l',
            'c': 'k', 'k': 'c',
            'đ': 'd', 'v': 'w', 'ph': 'f'
        }
        for key, value in typo_map.items():
            if char.startswith(key):
                return value + char[len(key):]
        return char

    def random_noise(char):
        noise_types = [
            lambda c: '',  # Delete character
            lambda c: c + c,  # Duplicate character
            lambda c: c + random.choice('abcdefghijklmnopqrstuvwxyz'),  # Add random character
            lambda c: unidecode.unidecode(c)  # Remove diacritics
        ]
        return random.choice(noise_types)(char)

    def apply_noise_to_char(char):
        if random.random() < noise_level:
            noise_type = random.choice(['swap_accent', 'common_typo', 'random_noise'])
            if noise_type == 'swap_accent':
                return swap_accent(char)
            elif noise_type == 'common_typo':
                return common_typo(char)
            else:
                return random_noise(char)
        return char

    words = text.split()
    for i, word in enumerate(words):
        if random.random() < noise_level:
            noise_type = random.choice(['char_noise', 'abbreviation', 'capitalization'])
            if noise_type == 'char_noise':
                words[i] = ''.join(apply_noise_to_char(c) for c in word)
            elif noise_type == 'abbreviation':
                words[i] = abbreviation_error(word)


    noisy_text = ' '.join(words)

    return noisy_text

# Ví dụ sử dụng
original_text = "Chào bạn, hôm nay thời tiết đẹp quá. Chúng ta đi dạo nhé?"
noisy_text = create_vietnamese_noise(original_text, noise_level=0.5)
print(f"Original: {original_text}")
print(f"Noisy   : {noisy_text}")