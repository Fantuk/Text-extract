# Для анализа структуры PDF и извлечения текста
from pdfminer.layout import LTTextContainer, LTChar

def text_extraction(element):
    # Извлекаем текст из вложенного текстового элемента
    line_text = element.get_text()
    
    # Находим форматы текста
    # Инициализируем список со всеми форматами, встречающимися в строке текста
    line_formats = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):

            # Итеративно обходим каждый символ в строке текста
            for character in text_line:
                if isinstance(character, LTChar):

                    # Добавляем к символу название шрифта
                    line_formats.append(character.fontname)

                    # Добавляем к символу размер шрифта
                    line_formats.append(round(character.size))

    # Находим уникальные размеры и названия шрифтов в строке
    format_per_line = list(set(line_formats))
    
    # Возвращаем кортеж с текстом в каждой строке вместе с его форматом
    return (line_text, format_per_line)