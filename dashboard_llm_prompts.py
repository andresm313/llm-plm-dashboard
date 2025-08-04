import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="PLM Dashboard with LLM Prompts", layout="wide")
st.title("🧩 PLM Dashboard + LLM Prompt Generator")

uploaded_file = st.file_uploader("Upload your PLM-style CSV file", type=["csv"])

templates = {
    "Summarize Change History": "Here is a dataset:\n\n{table}\n\nPlease summarize key change events, including major ECOs and lifecycle shifts.",
    "Impact Analysis": "Given the following engineering changes:\n\n{table}\n\nWhich assemblies or subassemblies are most impacted?",
    "Suggest Process Improvements": "Here is recent change and BOM data:\n\n{table}\n\nSuggest 2 ways to improve release-to-manufacturing efficiency.",
    "Freeform Prompt": "{custom}"
}

st.sidebar.header("Select Prompt Type")
prompt_type = st.sidebar.selectbox("Prompt Style", list(templates.keys()))

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Preview of Uploaded Data")
    st.dataframe(df.head(100), use_container_width=True)

    # ---------------- Visualizations ----------------
    st.markdown("## 📊 Visualizations")

    if "Lifecycle Phase" in df.columns:
        st.markdown("### Assemblies by Lifecycle Phase")
        lifecycle_counts = df["Lifecycle Phase"].value_counts().reset_index()
        lifecycle_counts.columns = ["Lifecycle Phase", "Count"]
        lifecycle_chart = alt.Chart(lifecycle_counts).mark_bar().encode(
            x="Lifecycle Phase:N",
            y="Count:Q",
            color="Lifecycle Phase:N"
        ).properties(width=600, height=300)
        st.altair_chart(lifecycle_chart, use_container_width=True)

    if "ECO Status" in df.columns:
        st.markdown("### Engineering Change Order (ECO) Status")
        eco_counts = df["ECO Status"].value_counts().reset_index()
        eco_counts.columns = ["ECO Status", "Count"]
        eco_chart = alt.Chart(eco_counts).mark_bar().encode(
            x="ECO Status:N",
            y="Count:Q",
            color="ECO Status:N"
        ).properties(width=600, height=300)
        st.altair_chart(eco_chart, use_container_width=True)

    if "BOM Status" in df.columns and "Revision" in df.columns:
        st.markdown("### BOM Status by Revision")
        bom_chart = alt.Chart(df).mark_boxplot().encode(
            x="Revision:N",
            y="BOM Status:Q",
            color="Revision:N"
        ).properties(width=600, height=300)
        st.altair_chart(bom_chart, use_container_width=True)

    if "CAD Preview" in df.columns:
        st.markdown("### CAD Preview Availability")
        cad_counts = df["CAD Preview"].value_counts().reset_index()
        cad_counts.columns = ["CAD Preview", "Count"]
        cad_chart = alt.Chart(cad_counts).mark_bar().encode(
            x="CAD Preview:N",
            y="Count:Q",
            color="CAD Preview:N"
        ).properties(width=600, height=300)
        st.altair_chart(cad_chart, use_container_width=True)

    # ---------------- Prompt Generation ----------------
    table_str = df.to_markdown(index=False)

    if prompt_type == "Freeform Prompt":
        custom_input = st.text_area("Enter your custom prompt (use {table} to insert data)", height=200)
        final_prompt = custom_input.replace("{table}", table_str)
    else:
        final_prompt = templates[prompt_type].replace("{table}", table_str)

    st.subheader("🧠 Generated Prompt for LLM")
    st.code(final_prompt, language="markdown")
    st.download_button("Download Prompt as .txt", data=final_prompt, file_name="llm_prompt.txt")
