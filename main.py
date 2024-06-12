from camelot import read_pdf
import pandas as pd
import sqlite3 as sl


def main():
    import_path = 'В3.pdf'            # Путь к pdf
    database_path = 'database.db'     # Путь к базе данных

    #Чтение файла
    tables = read_pdf(import_path, strip_text='\n', line_scale=40, pages='all', copy_text=['h'])
    if tables.n == 0:
        return "Не удалось извлечь данные"

    #Обьединение всех таблиц из pdf файла в один DataFrame
    whole_table = pd.DataFrame(None)
    for table in tables:
        whole_table = pd.concat([whole_table, table.df])

    # Удаление ненужных строк и столбцов
    whole_table.drop(index=whole_table.index[-1], axis=0, inplace=True)       # Удаление последней строки
    whole_table.drop(index=whole_table.index[0], axis=0, inplace=True)          # Удаление первой строки
    whole_table.drop(columns=whole_table.columns[0], axis=1, inplace=True)      # Удаление первого столбца
    whole_table['5'] = 0
    whole_table.columns = ["Адрес", "Начислено", "Оплачено", "Агентское вознаграждение", "Процент вознаграждения"]

    # Удаление пробелов
    whole_table["Агентское вознаграждение"] = whole_table["Агентское вознаграждение"].str.replace(' ', '')
    whole_table["Начислено"] = whole_table["Начислено"].str.replace(' ', '')
    whole_table["Оплачено"] = whole_table["Оплачено"].str.replace(' ', '')

    # Замена запятой на точку для приведения к вещественному типу
    whole_table["Агентское вознаграждение"] = whole_table["Агентское вознаграждение"].str.replace(',', '.')
    whole_table["Начислено"] = whole_table["Начислено"].str.replace(',', '.')
    whole_table["Оплачено"] = whole_table["Оплачено"].str.replace(',', '.')

    # Приведение данных к соответствующим типам
    whole_table["Адрес"] = whole_table["Адрес"].astype('string')
    whole_table["Начислено"] = whole_table["Начислено"].astype(float)
    whole_table["Оплачено"] = whole_table["Оплачено"].astype(float)
    whole_table["Агентское вознаграждение"] = whole_table["Агентское вознаграждение"].astype(float)

    # Вычисление процента агентского вознаграждения
    whole_table["Процент вознаграждения"] = whole_table["Агентское вознаграждение"] * 100 / whole_table["Начислено"]
    whole_table["Процент вознаграждения"] = whole_table["Процент вознаграждения"].round(1)

    # Экспорт таблицы в базу данных
    con = sl.connect(database_path)
    whole_table.to_sql('payments', con, if_exists='replace', index=False)
    con.commit()
    con.close()


if __name__ == '__main__':
    main()

