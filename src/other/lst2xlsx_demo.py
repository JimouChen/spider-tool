import pandas as pd


def lst2xlsx(
        data: list[dict],
        excel_path: str,
        col_width: dict = None,
        sheet_name: str = "Sheet1"
):
    df = pd.DataFrame(data)
    with pd.ExcelWriter(excel_path, engine='xlsxwriter', engine_kwargs={
        'options': {'strings_to_formulas': False}
    }) as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
        worksheet = writer.sheets[sheet_name]
        for idx, col in enumerate(df.columns):
            if col_width and col in col_width:
                width = col_width[col]
            else:
                width = len(col) + 10

            worksheet.set_column(idx, idx, width)


# 示例用法
data_ = [
    {'Name': 'Alice', 'Age': 30, 'City': 'New York'},
    {'Name': 'Bob', 'Age': 25, 'City': 'Los Angeles'}
]

lst2xlsx(data_, './data/output1.xlsx')
