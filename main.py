import camelot
import pandas as pd


def main():
    import_path = 'В3.pdf'            # Путь к pdf
    export_path = 'ResultTable.xlsx'  # Путь к excel

    #Чтение файла
    tables = camelot.read_pdf(import_path, strip_text='\n', line_scale=40, pages='all', copy_text=['h'])
    if tables.n == 0:
        return "Не удалось извлечь данные"

    whole_table = pd.DataFrame(None)
    for table in tables:
        whole_table = pd.concat([whole_table, table.df])

    whole_table.drop(index=whole_table.index[-1], axis=0, inplace=True)       # Удаление последней строки
    whole_table.drop(index=whole_table.index[0], axis=0, inplace=True)          # Удаление первой строки
    whole_table.drop(columns=whole_table.columns[0], axis=1, inplace=True)      # Удаление первого столбца
    whole_table["5"] = 0
    whole_table.columns = ["Адрес", "Начислено", "Оплачено", "Агентское вознаграждение", "Процент вознаграждения"]
    whole_table["Агентское вознаграждение"] = whole_table["Агентское вознаграждение"].str.replace(' ', '')
    whole_table["Начислено"] = whole_table["Начислено"].str.replace(' ', '')
    whole_table["Процент вознаграждения"] = whole_table["Агентское вознаграждение"].str.replace(',', '.').astype(float) * 100 / whole_table["Начислено"].str.replace(',', '.').astype(float)
    whole_table.to_excel(export_path, index=False, header=True)


if __name__ == '__main__':
    main()

