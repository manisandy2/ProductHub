import pandas as pd


class ExcelWriter:

    @staticmethod
    def save(data, file_path):

        df = pd.DataFrame(data)

        df.to_excel(
            file_path,
            index=False
        )