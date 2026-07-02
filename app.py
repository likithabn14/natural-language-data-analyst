import streamlit as st
import pandas as pd
import duckdb

from sql_generator import generate_sql
from export import export_csv, export_excel, export_pdf
from examples import generate_examples


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Natural Language Data Analyst",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# Load CSS
# --------------------------------------------------

try:
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
except:
    pass


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "question" not in st.session_state:
    st.session_state.question = ""


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    "<div class='main-title'>📊 Natural Language Data Analyst</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>Analyze CSV files using simple English queries</div>",
    unsafe_allow_html=True
)

st.divider()


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("Project")

    st.write("Natural Language Data Analyst")

    st.divider()

    st.subheader("Features")

    st.write("✅ Upload CSV")
    st.write("✅ SQL Generator")
    st.write("✅ Charts")
    st.write("✅ Statistics")
    st.write("✅ Export Results")

    st.divider()

    st.info(
        "Upload a CSV file to begin."
    )


# --------------------------------------------------
# Upload CSV
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is None:

    st.info("Please upload a CSV file.")

    st.stop()


# --------------------------------------------------
# Read Dataset
# --------------------------------------------------

try:

    df = pd.read_csv(uploaded_file)

except Exception as e:

    st.error(f"Unable to read CSV.\n\n{e}")

    st.stop()


st.success("Dataset Loaded Successfully!")

duckdb.register("dataset", df)


# --------------------------------------------------
# Dataset Preview
# --------------------------------------------------

with st.expander("📋 Dataset Preview", expanded=True):

    st.dataframe(
        df.head(10),
        use_container_width=True
    )


# --------------------------------------------------
# Dataset Information
# --------------------------------------------------

with st.expander("📑 Dataset Information"):

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])
    c3.metric("Missing Values", int(df.isnull().sum().sum()))
    c4.metric("Duplicate Rows", int(df.duplicated().sum()))


# --------------------------------------------------
# Dataset Schema
# --------------------------------------------------
schema = pd.DataFrame({
    "Column Name": df.columns,
    "Data Type": df.dtypes.astype(str).values
})
with st.expander("📚 Dataset Schema"):

    st.dataframe(
        schema,
        use_container_width=True
    )


# --------------------------------------------------
# Example Questions
# --------------------------------------------------

examples = generate_examples(df)

st.subheader("💡 Quick Example Questions")

# ==========================
# Basic Queries
# ==========================

with st.expander("📄 Basic Queries", expanded=True):

    basic = [
        q for q in examples
        if q in [
            "Show all data",
            "Top 10 rows",
            "Top 5 rows",
            "Count rows"
        ]
    ]

    cols = st.columns(2)

    for i, q in enumerate(basic):

        with cols[i % 2]:

            if st.button(q, key=f"basic_{i}"):

                st.session_state.question = q
                st.session_state.run_query = True
                st.rerun()


# ==========================
# Aggregate & Analysis Queries
# ==========================

with st.expander("📊 Aggregate & Analysis Queries"):

    analysis = [
        q for q in examples
        if q not in [
            "Show all data",
            "Top 10 rows",
            "Top 5 rows",
            "Count rows"
        ]
        and "Sort by" not in q
    ]

    cols = st.columns(2)

    for i, q in enumerate(analysis):

        with cols[i % 2]:

            if st.button(q, key=f"analysis_{i}"):

                st.session_state.question = q
                st.session_state.run_query = True
                st.rerun()


# --------------------------------------------------
# Ask Question
# --------------------------------------------------
st.markdown("---")
st.header("🔍 Ask your question")

question = st.text_input(
    "Ask your question",
    value=st.session_state.question,
    placeholder="Example: Show total Sales by Country"
)


if not question:

    st.stop()


st.divider()


# --------------------------------------------------
# Generate SQL
# --------------------------------------------------

sql, chart_type = generate_sql(
    question,
    df
)


if sql is None:

    st.error(
        "Sorry! I couldn't understand your question."
    )

    st.stop()


st.subheader("📝 Generated SQL")

st.code(
    sql,
    language="sql"
)
# --------------------------------------------------
# Execute SQL
# --------------------------------------------------

try:

    result_df = duckdb.sql(sql).df()

except Exception as e:

    st.error(f"SQL Error:\n\n{e}")

    st.stop()


# --------------------------------------------------
# Query Result
# --------------------------------------------------

st.subheader("Query Result")

# Single Value Result
if result_df.shape == (1, 1):

    value = result_df.iloc[0, 0]

    label = result_df.columns[0]

    if isinstance(value, float):
        value = f"{value:,.2f}"

    elif isinstance(value, int):
        value = f"{value:,}"

    st.metric(label, value)

else:

    st.dataframe(
        result_df,
        use_container_width=True
    )
st.divider()

# --------------------------------------------------
# Statistics
# --------------------------------------------------

st.subheader("Statistics")

numeric = result_df.select_dtypes(include="number")

if numeric.empty:

    st.info("No numeric columns found.")

else:

    st.dataframe(
        numeric.describe().T,
        use_container_width=True
    )

st.divider()


# --------------------------------------------------
# Downloads
# --------------------------------------------------

st.subheader("Download Results")

csv_file = export_csv(result_df)
excel_file = export_excel(result_df)
pdf_file = export_pdf(result_df)

col1, col2, col3 = st.columns(3)

with col1:

    st.download_button(
        "📄 Download CSV",
        csv_file,
        file_name="query_result.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:

    st.download_button(
        "📊 Download Excel",
        excel_file,
        file_name="query_result.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

with col3:

    st.download_button(
        "📕 Download PDF",
        pdf_file,
        file_name="query_result.pdf",
        mime="application/pdf",
        use_container_width=True
    )

st.divider()


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown(
    """
    <div style='text-align:center;
                color:gray;
                padding:20px;
                font-size:15px;'>

    📊 Natural Language Data Analyst <br>
    Built with Python • Streamlit • DuckDB • Plotly

    </div>
    """,
    unsafe_allow_html=True
)