import unittest
import os
import pandas as pd

from plantpredict.helpers import load_from_excel, export_to_excel


class TestHelpers(unittest.TestCase):
    def setUp(self):
        self.data = [
            {"Index": 1, "Name": "Stephen", "City": "Denver, CO"},
            {"Index": 2, "Name": "Kendra", "City": "Denver, CO"},
            {"Index": 3, "Name": "Sam", "City": "San Francisco, CA"},
            {"Index": 4, "Name": "Alex", "City": "Tempe, AZ"}
        ]

    def test_export_to_excel(self):
        export_to_excel(
            data=self.data,
            file_path="test_data/testing_helpers.xlsx",
            field_order=["Index", "Name", "City"],
            sorting_fields=["Index"]
        )

        self.assertTrue(os.path.exists("test_data/testing_helpers.xlsx"))

        xl = pd.ExcelFile("test_data/testing_helpers.xlsx")
        xl_truth = pd.ExcelFile("test_data/testing_helpers_truth.xlsx")
        self.assertEqual(
            xl.parse("Sheet1", index_col=None).to_dict('records'),
            xl_truth.parse("Sheet1", index_col=None).to_dict('records')
        )

        os.remove("test_data/testing_helpers.xlsx")

    def test_export_to_excel_with_sheet_name(self):
        export_to_excel(
            data=self.data,
            file_path="test_data/testing_helpers.xlsx",
            sheet_name="Sheet Name",
            field_order=["Index", "Name", "City"],
            sorting_fields=["Index"]
        )

        self.assertTrue(os.path.exists("test_data/testing_helpers.xlsx"))

        xl = pd.ExcelFile("test_data/testing_helpers.xlsx")
        xl_truth = pd.ExcelFile("test_data/testing_helpers_truth.xlsx")
        self.assertEqual(
            xl.parse("Sheet Name", index_col=None).to_dict('records'),
            xl_truth.parse("Sheet1", index_col=None).to_dict('records')
        )

        os.remove("test_data/testing_helpers.xlsx")

    def test_load_from_excel(self):
        loaded_data = load_from_excel("test_data/testing_helpers_truth.xlsx")
        self.assertEqual(loaded_data, self.data)

    def test_load_from_excel_with_sheet_name(self):
        loaded_data = load_from_excel("test_data/testing_helpers_truth.xlsx", "Sheet1")
        self.assertEqual(loaded_data, self.data)


if __name__ == '__main__':
    unittest.main()
