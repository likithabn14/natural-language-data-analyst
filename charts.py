import pandas as pd
import plotly.express as px


def create_chart(df, chart_type="auto"):
    """
    Create charts automatically based on query result.
    """

    # -----------------------------------
    # Empty Result
    # -----------------------------------

    if df is None or df.empty:
        return None

    # -----------------------------------
    # One Column (Single Value)
    # -----------------------------------

    if len(df.columns) == 1:

        col = df.columns[0]

        if pd.api.types.is_numeric_dtype(df[col]):

            fig = px.bar(
                x=[col],
                y=[df.iloc[0, 0]],
                text=[f"{df.iloc[0,0]:,.2f}" if isinstance(df.iloc[0,0], float)
                      else f"{df.iloc[0,0]:,}"],
                title=col
            )

            fig.update_traces(textposition="outside")

            fig.update_layout(
                xaxis_title="",
                yaxis_title=col,
                showlegend=False,
                height=450
            )

            return fig

        return None

    # -----------------------------------
    # Two Columns
    # -----------------------------------

    if len(df.columns) == 2:

        x = df.columns[0]
        y = df.columns[1]

        # Numeric + Numeric
        if (
            pd.api.types.is_numeric_dtype(df[x]) and
            pd.api.types.is_numeric_dtype(df[y])
        ):

            return px.scatter(
                df,
                x=x,
                y=y,
                title=f"{y} vs {x}"
            )

        # Second column must be numeric
        if not pd.api.types.is_numeric_dtype(df[y]):
            return None

        # Force Bar
        if chart_type == "bar":

            return px.bar(
                df,
                x=x,
                y=y,
                text_auto=True,
                title=f"{y} by {x}"
            )

        # Force Pie
        if chart_type == "pie":

            return px.pie(
                df,
                names=x,
                values=y,
                title=f"{y} by {x}"
            )

        # Force Line
        if chart_type == "line":

            return px.line(
                df,
                x=x,
                y=y,
                markers=True,
                title=f"{y} by {x}"
            )

        # AUTO

        if len(df) <= 6:

            return px.pie(
                df,
                names=x,
                values=y,
                title=f"{y} by {x}"
            )

        elif len(df) <= 20:

            return px.bar(
                df,
                x=x,
                y=y,
                text_auto=True,
                title=f"{y} by {x}"
            )

        else:

            return px.line(
                df,
                x=x,
                y=y,
                markers=True,
                title=f"{y} Trend"
            )

    # -----------------------------------
    # More than Two Columns
    # -----------------------------------

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if len(numeric_cols) == 0:
        return None

    x = df.columns[0]
    y = numeric_cols[0]

    return px.bar(
        df,
        x=x,
        y=y,
        text_auto=True,
        title=f"{y} by {x}"
    )