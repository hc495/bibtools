def capitalize_title(title):
    lowercase_words = {'and', 'in', 'the', 'of', 'a', 'an', 'to', 'with', 'for', 'on', 'at', 'by', 'from', 'via', 'as', 'into', 'onto', 'upon', 'but', 'nor', 'or', 'so'}
    words = title.split()
    capitalized_words = []
    for i, word in enumerate(words):
        if word.isupper():  # 如果词本身是全大写（如 NASA），保持不变
            capitalized_words.append(word)
        elif i == 0 or word.lower() not in lowercase_words:
            capitalized_words.append(word.capitalize())
        else:
            capitalized_words.append(word.lower())
    return ' '.join(capitalized_words)
    capitalized_words = [word.capitalize() if word.lower() not in lowercase_words else word.lower() for word in words]
    capitalized_words[0] = capitalized_words[0].capitalize()  # Always capitalize the first word
    return ' '.join(capitalized_words)

def lowercase_title(title):
    title = title.replace('{', '').replace('}', '')

    words = title.split()
    normalized_words = []

    for word in words:
        if any(word[i].isupper() and word[i + 1].isupper() for i in range(len(word) - 1)):
            normalized_words.append(word)
        else:
            normalized_words.append(word.lower())

    result = ' '.join(normalized_words)

    for i, ch in enumerate(result):
        if ch.isalpha():
            result = result[:i] + ch.upper() + result[i + 1:]
            break

    return result
