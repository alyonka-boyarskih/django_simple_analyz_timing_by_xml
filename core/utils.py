import os
from datetime import datetime, date
from typing import List, TextIO

import pandas as pd
import xml.etree.ElementTree as et

from loguru import logger


def parse_xml_convert_to_data_frame(xml_file_path: TextIO, df_column_names: List[str]):

    xtree = et.parse(xml_file_path)
    xroot = xtree.getroot()
    rows = []

    for node in xroot:
        res = [node.attrib.get(df_column_names[0])]

        for element in df_column_names[1:]:
            if node is not None and node.find(element) is not None:
                element_text = node.find(element).text
                if element in ["start", "end"]:
                    element_text = datetime.strptime(element_text, "%d-%m-%Y %H:%M:%S")
                res.append(element_text)
            else:
                res.append(None)
        rows.append({
            df_column_names[i]: res[i] for i, _ in enumerate(df_column_names)
        })

    out_df = pd.DataFrame(rows, columns=df_column_names)
    logger.info(out_df)
    return out_df


def analyz_by_data_frame(data_frame: pd.DataFrame, date_start: date, date_end: date):
    logger.info("ANALYZE DATA FRAME")
    logger.info("   --CREATE CLUMNS 'TIMING' - difference between start and end arriving datetime")
    data_frame["timing"] = data_frame["end"] - data_frame["start"]
    logger.info(data_frame)

    data_frame = data_frame.loc[data_frame["start"].dt.date.between(date_start, date_end)]
    if data_frame.empty:
        return data_frame

    logger.info("   --GROUP BY COLUMNS 'FULL_NAME'")

    dt_new: pd.DataFrame = data_frame.groupby([data_frame.full_name], as_index=False).first()
    dt_new["timing"] = data_frame.groupby([data_frame.full_name], as_index=False)["timing"].sum()["timing"]
    logger.info(dt_new)
    return dt_new


def get_files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file
