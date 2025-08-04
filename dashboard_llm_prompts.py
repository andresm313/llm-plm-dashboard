import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="PLM Dashboard with LLM Prompt Generator", layout="wide")
st.title("🧠 PLM Dashboard + LLM Prompt Generator")

# File uploader
uploaded_file = st.file_uploader("📤 Upload your PLM CSV file", type=["csv"])

# Prompt templates
templates = {
    "Summarize Changes": "Here is a dataset:\n\n{table}\n\nPlease summarize the recent product changes and their status.",
    "Change Impact Analysis": "Given the following PLM data:\n\n{table}\n\nIdentify impacted assemblies and teams from recent ECOs.",
    "Suggest Improvements": "Here is a dataset:\n\n{table}\n\nIdentify potential process improvements for change cycles.",
    "Freeform Prompt": "{custom}"
}

st.sidebar.header("🧰 Prompt Generator")
prompt_type = st.sidebar.selectbox("Select Prompt Type", list(templates.keys()))

# If a file is uploaded
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Data Preview")
    st.dataframe(df.head(100), use_container_width=True)

    st.markdown("## 📊 Visualizations")

    # Lifecycle Phase Visualization
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

    # ECO Status Visualization
    if "ECO Status" in df.columns:
        st.markdown("### ECOs by Status")
        eco_counts = df["ECO Status"].value_counts().reset_index()
        eco_counts.columns = ["ECO Status", "Count"]
        eco_chart = alt.Chart(eco_counts).mark_bar().encode(
            x="ECO Status:N",
            y="Count:Q",
            color="ECO Status:N"
        ).properties(width=600, height=300)
        st.altair_chart(eco_chart, use_container_width=True)

    # Mockup CAD File Preview
    st.markdown("### 🧷 CAD File Preview")
    st.image("mock_cad_preview.png", caption="CAD Drawing - Assembly 102-RevB", use_column_width=True)

    # Generate prompt
    table_str = df.to_markdown(index=False)

    if prompt_type == "Freeform Prompt":
        custom_input = st.text_area("✍️ Enter your custom prompt (use {table} to insert data)", height=200)
        final_prompt = custom_input.replace("{table}", table_str)
    else:
        final_prompt = templates[prompt_type].replace("{table}", table_str)

    st.subheader("🧠 Generated Prompt")
    st.code(final_prompt, language="markdown")
    st.download_button("📥 Download Prompt as .txt", data=final_prompt, file_name="llm_prompt.txt")
else:
    st.info("👆 Please upload a PLM CSV file to begin.")
