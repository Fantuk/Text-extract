# Для считывания PDF
import PyPDF2 

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTRect

# Для извлечения текста из таблиц в PDF
import pdfplumber

#Импортируем функцию извлечения текста
from text_extaction_func import text_extraction

#Импортируем функции извлечения и форматирования таблиц
from table_text_extaction_func import extract_table, table_converter


pdf_path = "./text.pdf"

# создаём объект файла PDF
pdfFileObj = open(pdf_path, 'rb')

# создаём объект считывателя PDF
pdfReaded = PyPDF2.PdfReader(pdfFileObj)

# Создаём словарь для извлечения текста из каждой страницы
text_per_page = {}
            
# Извлекаем страницы из PDF
for pagenum, page in enumerate(extract_pages(pdf_path)):

    pageObj = pdfReaded.pages[pagenum]
    page_text = []
    line_format = []
    text_from_tables = []
    page_content = []

    # Инициализируем количество исследованных таблиц
    table_num = 0
    first_element= True
    table_extraction_flag= False

    # Открываем файл pdf
    pdf = pdfplumber.open(pdf_path)

    # Находим исследуемую страницу
    page_tables = pdf.pages[pagenum]

    # Находим количество таблиц на странице
    tables = page_tables.find_tables()

    # Находим все элементы
    page_elements = [(element.y1, element) for element in page._objs]
    # Сортируем все элементы по порядку нахождения на странице
    page_elements.sort(key=lambda a: a[0], reverse=True)

    # Находим элементы, составляющие страницу
    for i,component in enumerate(page_elements):
        # Извлекаем положение верхнего края элемента в PDF
        pos= component[0]
        # Извлекаем элемент структуры страницы
        element = component[1]

         # Проверяем, является ли элемент текстовым
        if isinstance(element, LTTextContainer):

            # Проверяем, находится ли текст в таблице
            if table_extraction_flag == False:

                # Используем функцию извлечения текста и формата для каждого текстового элемента
                (line_text, format_per_line) = text_extraction(element)

                # Добавляем текст каждой строки к тексту страницы
                page_text.append(line_text)

                # Добавляем формат каждой строки, содержащей текст
                line_format.append(format_per_line)
                page_content.append(line_text)

        else:
            pass

        # Проверяем элементы на наличие таблиц
        if isinstance(element, LTRect):

            # Если первый прямоугольный элемент
            if first_element == True and (table_num+1) <= len(tables):

                # Находим ограничивающий прямоугольник таблицы
                lower_side = page.bbox[3] - tables[table_num].bbox[3]
                upper_side = element.y1 

                # Извлекаем информацию из таблицы
                table = extract_table(pdf_path, pagenum, table_num)

                # Конвертируем таблицу в строку
                table_string = table_converter(table)

                # Добавляем строку таблицы в список
                text_from_tables.append(table_string)
                page_content.append(table_string)

                # Устанавливаем флаг True, чтобы избежать повторения содержимого
                table_extraction_flag = True

                # Преобразуем в другой элемент
                first_element = False

                # Добавляем условное обозначение в списки текста и формата
                page_text.append('table')
                line_format.append('table')

            # Проверяем, извлекли ли мы уже таблицы из этой страницы
            if element.y0 >= lower_side and element.y1 <= upper_side:
                pass
            elif not isinstance(page_elements[i+1][1], LTRect):
                table_extraction_flag = False
                first_element = True
                table_num+=1

    # Создаём ключ для словаря
    dctkey = 'Page_'+str(pagenum)

    # Добавляем список списков как значение ключа страницы
    text_per_page[dctkey]= [page_text, line_format, text_from_tables, page_content]

# Закрываем объект файла pdf
pdfFileObj.close()


print(text_per_page)
