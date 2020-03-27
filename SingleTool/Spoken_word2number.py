import re

_known = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'fourty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90
}


def spoken_word_to_number(n):
    try:
        n = n.lower().strip()
        if n in _known:
            return _known[n]
        else:
            input_word_arr = re.split(r'[\s, -, _]', n)
        assert len(input_word_arr) > 1  # all single words are known
        # Check the pathological case where hundred is at the end or thousand is at end
        if input_word_arr[-1] == 'hundred':
            input_word_arr.append('zero')
            input_word_arr.append('zero')
        if input_word_arr[-1] == 'thousand':
            input_word_arr.append('zero')
            input_word_arr.append('zero')
            input_word_arr.append('zero')
        if input_word_arr[0] == 'hundred':
            input_word_arr.insert(0, 'one')
        if input_word_arr[0] == 'thousand':
            input_word_arr.insert(0, 'one')
        input_word_arr = [word for word in input_word_arr if word not in ['and', 'minus', 'negative']]
        current_position = 'unit'
        output = 0
        for word in reversed(input_word_arr):
            if current_position == 'unit':
                number = _known[word]
                output += number
                if number > 9:
                    current_position = 'hundred'
                else:
                    current_position = 'ten'
            elif current_position == 'ten':
                if word != 'hundred':
                    number = _known[word]
                    if number < 10:
                        output += number * 10
                    else:
                        output += number
                # else: nothing special
                current_position = 'hundred'
            elif current_position == 'hundred':
                if word not in ['hundred', 'thousand']:
                    number = _known[word]
                    output += number * 100
                    current_position = 'thousand'
                elif word == 'thousand':
                    current_position = 'thousand'
                else:
                    current_position = 'hundred'
            elif current_position == 'thousand':
                assert word != 'hundred'
                if word != 'thousand':
                    number = _known[word]
                    output += number * 1000
            else:
                assert "Can't be here" is None
    except:
        output = n
    return output


if __name__ == '__main__':
    print(spoken_word_to_number('fourty_nine'))
