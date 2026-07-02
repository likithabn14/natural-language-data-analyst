import re


def generate_sql(question, df):

    question = question.lower().strip()

    columns = df.columns.tolist()

    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    text_columns = df.select_dtypes(exclude="number").columns.tolist()

    chart_type = "auto"

    # ----------------------------------------
    # Helper Functions
    # ----------------------------------------

    def get_numeric_column(text):

        text = text.lower()

        for col in numeric_columns:

            if col.lower() == text:
                return col

            if col.lower() in text:
                return col

        return None

    def get_text_column(text):

        text = text.lower()

        for col in text_columns:

            if col.lower() == text:
                return col

            if col.lower() in text:
                return col

        return None

    # ----------------------------------------
    # SHOW ALL DATA
    # ----------------------------------------

    if question in [
        "show all",
        "show all data",
        "display all data",
        "display dataset",
        "show dataset"
    ]:

        sql = """
SELECT *
FROM dataset;
"""

        return sql, None

    # ----------------------------------------
    # COUNT ROWS
    # ----------------------------------------

    if any(x in question for x in [
        "count rows",
        "number of rows",
        "count",
        "total rows"
    ]):

        sql = """
SELECT COUNT(*) AS Total_Rows
FROM dataset;
"""

        return sql, None

    # ----------------------------------------
    # TOP N ROWS
    # ----------------------------------------

    top = re.search(r"top\s+(\d+)", question)

    if top:

        n = int(top.group(1))

        # Top N rows

        if "by" not in question:

            sql = f"""
SELECT *
FROM dataset
LIMIT {n};
"""

            return sql, None

        # Top N rows by Column

        if "rows by" in question:

            col_name = question.split("rows by")[1].strip()

            for col in columns:

                if col.lower() == col_name.lower():

                    sql = f'''
SELECT *
FROM dataset
ORDER BY "{col}" DESC
LIMIT {n};
'''

                    return sql, None

    # ----------------------------------------
    # MAXIMUM
    # ----------------------------------------

    if any(x in question for x in [
        "maximum",
        "highest",
        "max"
    ]):

        col = get_numeric_column(question)

        if col:

            sql = f'''
SELECT
MAX("{col}") AS Maximum
FROM dataset;
'''

            return sql, None

    # ----------------------------------------
    # MINIMUM
    # ----------------------------------------

    if any(x in question for x in [
        "minimum",
        "lowest",
        "min"
    ]):

        col = get_numeric_column(question)

        if col:

            sql = f'''
SELECT
MIN("{col}") AS Minimum
FROM dataset;
'''

            return sql, None

    # ----------------------------------------
    # AVERAGE
    # ----------------------------------------

    if any(x in question for x in [
        "average",
        "avg",
        "mean"
    ]):

        col = get_numeric_column(question)

        if col:

            sql = f'''
SELECT
AVG("{col}") AS Average
FROM dataset;
'''

            return sql, None

    # ----------------------------------------
    # TOTAL
    # ----------------------------------------

    if any(x in question for x in [
        "total",
        "sum"
    ]):

        col = get_numeric_column(question)

        if col:

            sql = f'''
SELECT
SUM("{col}") AS Total
FROM dataset;
'''

            return sql, None
            # ----------------------------------------
    # GROUP BY
    # Example:
    # Show total Sales by Country
    # Show average Profit by Region
    # ----------------------------------------

    if " by " in question:

        parts = question.split(" by ")

        if len(parts) == 2:

            left = parts[0].strip()
            right = parts[1].strip()

            value_col = get_numeric_column(left)
            group_col = get_text_column(right)

            if value_col and group_col:

                # TOTAL

                if "total" in left or "sum" in left:

                    sql = f'''
SELECT
    "{group_col}",
    SUM("{value_col}") AS Total
FROM dataset
GROUP BY "{group_col}"
ORDER BY Total DESC;
'''

                    return sql, "bar"

                # AVERAGE

                if (
                    "average" in left
                    or "avg" in left
                    or "mean" in left
                ):

                    sql = f'''
SELECT
    "{group_col}",
    AVG("{value_col}") AS Average
FROM dataset
GROUP BY "{group_col}"
ORDER BY Average DESC;
'''

                    return sql, "bar"

                # MAXIMUM

                if (
                    "maximum" in left
                    or "highest" in left
                    or "max" in left
                ):

                    sql = f'''
SELECT
    "{group_col}",
    MAX("{value_col}") AS Maximum
FROM dataset
GROUP BY "{group_col}"
ORDER BY Maximum DESC;
'''

                    return sql, "bar"

                # MINIMUM

                if (
                    "minimum" in left
                    or "lowest" in left
                    or "min" in left
                ):

                    sql = f'''
SELECT
    "{group_col}",
    MIN("{value_col}") AS Minimum
FROM dataset
GROUP BY "{group_col}"
ORDER BY Minimum ASC;
'''

                    return sql, "bar"

    # ----------------------------------------
    # TOP N CATEGORY BY VALUE
    # Example:
    # Top 5 Country by Sales
    # Top 10 Region by Profit
    # ----------------------------------------

    top_match = re.search(r"top\s+(\d+)", question)

    if top_match and " by " in question:

        n = int(top_match.group(1))

        parts = question.split(" by ")

        if len(parts) == 2:

            left = parts[0]
            right = parts[1]

            group_col = get_text_column(left)
            value_col = get_numeric_column(right)

            if group_col and value_col:

                sql = f'''
SELECT
    "{group_col}",
    SUM("{value_col}") AS Total
FROM dataset
GROUP BY "{group_col}"
ORDER BY Total DESC
LIMIT {n};
'''

                return sql, "bar"

# ----------------------------------------
# SORT
# ----------------------------------------

    if question.startswith("sort by"):
        text = question.replace("sort by", "").strip()

    order = "ASC"

    if text.endswith("descending"):
        order = "DESC"
        text = text.replace("descending", "").strip()

    elif text.endswith("ascending"):
        order = "ASC"
        text = text.replace("ascending", "").strip()

    for col in columns:

        col_lower = col.lower().strip()

        if (
            text.lower() == col_lower
            or text.lower() in col_lower
            or col_lower in text.lower()
        ):

            sql = f'''
SELECT *
FROM dataset
ORDER BY "{col}" {order};
'''

            return sql, None