# io module placeholder
# engine/io.py
import pandas as pd
from pathlib import Path

def load_table(path):
    p = Path(path)
    if p.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(p)
    elif p.suffix.lower() == ".csv":
        return pd.read_csv(p)
    else:
        raise ValueError(f"不支持的文件格式: {p.suffix}")