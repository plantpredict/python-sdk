import pandas as pd


def load_from_excel(file_path, sheet_name=None):
    """
    Loads the data from an Excel file into a list of dictionaries, where each dictionary represents a row in the Excel
    file and the keys of each dictionary represent each column header in the Excel file. The method creates this list
    of dictionaries via a Pandas dataframe.

    :param file_path: The full file path (appended with .xlsx) of the Excel file to be loaded.
    :type file_path: str
    :param sheet_name: Name of a particular sheet in the file to load (optional, defaults to the first sheet in the
    Excel file).
    :type sheet_name: str
    :return: List of dictionaries, each dictionary representing a row in the Excel file.
    :rtype: list of dict
    """
    xl = pd.ExcelFile(file_path)
    sheet_name = sheet_name if sheet_name else xl.sheet_names[0]

    return xl.parse(sheet_name, index_col=None).to_dict('records')


def export_to_excel(data, file_path, sheet_name="Sheet1", field_order=None, sorting_fields=None):
    """
    Writes data from a list of dictionaries to an Excel file, where each dictionary represents a row in the Excel file
    and the keys of each dictionary represent each column header in the Excel file.

    :param data: List of dictionaries, each dictionary representing a row in the Excel file.
    :type data: list of dict
    :param file_path: The full file path (appended with .xlsx) of the Excel file to be written to. This will overwrite
    data if both file_path and sheet_name already exist.
    :type file_path: str
    :param sheet_name: Name of a particular sheet in the file to write to (optional, defaults to "Sheet1").
    :type sheet_name: str
    :param field_order: List of keys from data ordered to match the intended Excel column ordering (left to right). Must
    include all keys/columns. Any keys omitted from the list will not be written as columns. (optional)
    :type field_order: list of str
    :param sorting_fields: List of keys from data to be used as sorting columns (small to large) in Excel. Can be any
    length from 1 column to every column. The order of the list will dictate the sorting order.
    :type sorting_fields: list of str
    :return: None
    """

    writer = pd.ExcelWriter(file_path, engine='openpyxl')
    df = pd.DataFrame(data)
    if field_order:
        df = df[field_order]
    if sorting_fields:
        df = df.sort_values(sorting_fields)
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()
