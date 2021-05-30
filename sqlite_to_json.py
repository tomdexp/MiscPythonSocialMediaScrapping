import pandas as pd
import sys
import json

def csvToJson():
    csv_file = "table_post_sql.csv"
    json_file = "table_post_records.json"
    data = pd.read_csv(csv_file, encoding="UTF-8")
    print(data)
    try:
        data.to_json(json_file, orient="records")
        print("done")
    except PermissionError:
        print("Please close the csv file before running the script ! Exiting...")
        sys.exit(1)
    return

csvToJson()