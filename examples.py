import pandas as pd


def generate_examples(df):

    examples = []

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    text_cols = df.select_dtypes(exclude="number").columns.tolist()

    # -------------------------
    # Basic
    # -------------------------

    examples.extend([
        "Show all data",
        "Top 10 rows",
        "Top 5 rows",
        "Count rows"
    ])

    # -------------------------
    # Numeric Examples
    # -------------------------

    if numeric_cols:

        num = numeric_cols[0]

        examples.extend([
            f"Show total {num}",
            f"Show average {num}",
            f"Show maximum {num}",
            f"Show minimum {num}",
            f"Sort by {num} ascending",
            f"Sort by {num} descending",
            f"Top 5 rows by {num}",
            f"Top 10 rows by {num}"
        ])

    # -------------------------
    # Grouped Examples
    # -------------------------

    if numeric_cols and text_cols:

        num = numeric_cols[0]
        cat = text_cols[0]

        examples.extend([
            f"Show total {num} by {cat}",
            f"Show average {num} by {cat}",
            f"Show maximum {num} by {cat}",
            f"Show minimum {num} by {cat}",
            f"Top 5 {cat} by {num}",
            f"Top 10 {cat} by {num}"
        ])

    # -------------------------
    # Second Text Column
    # -------------------------

    if numeric_cols and len(text_cols) > 1:

        num = numeric_cols[0]
        cat = text_cols[1]

        examples.extend([
            f"Show total {num} by {cat}",
            f"Show average {num} by {cat}",
            f"Top 5 {cat} by {num}"
        ])

    # -------------------------
    # Unique
    # -------------------------

    if text_cols:

        examples.append(f"Show unique {text_cols[0]}")

    # -------------------------
    # Remove duplicates
    # -------------------------

    unique = []

    for q in examples:

        if q not in unique:
            unique.append(q)

    return unique