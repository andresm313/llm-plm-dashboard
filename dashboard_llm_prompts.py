import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="PLM Dashboard with LLM Prompt Generator", layout="wide")
st.title("🧠 PLM Dashboard + LLM Prompt Generator")

# Upload section for main PLM data and BOM file
uploaded_file = st.file_uploader("📤 Upload your PLM CSV file", type=["csv"])
uploaded_bom = st.file_uploader("📘 Upload your BOM CSV file", type=["csv"])

# Prompt templates
templates = {
    "Summarize Changes": "Here is a dataset:\n\n{table}\n\nPlease summarize the recent product changes and their status.",
    "Change Impact Analysis": "Given the following PLM data:\n\n{table}\n\nIdentify impacted assemblies and teams from recent ECOs.",
    "Suggest Improvements": "Here is a dataset:\n\n{table}\n\nIdentify potential process improvements for change cycles.",
    "Freeform Prompt": "{custom}"
}

st.sidebar.header("🧰 Prompt Generator")
prompt_type = st.sidebar.selectbox("Select Prompt Type", list(templates.keys()))

# Main PLM file logic
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 PLM Data Preview")
    st.dataframe(df.head(100), use_container_width=True)

    # Optional filtering by user
    user_column = None
    if "User" in df.columns or "Modified By" in df.columns:
        user_column = "User" if "User" in df.columns else "Modified By"
        selected_user = st.selectbox("🔍 Filter by User", sorted(df[user_column].dropna().unique()))
        filtered_df = df[df[user_column] == selected_user]
        st.markdown(f"### 📄 Changes by {selected_user}")
        st.dataframe(filtered_df, use_container_width=True)

    # Visualizations
    st.markdown("## 📊 Visualizations")
    if user_column:
        user_counts = df[user_column].value_counts().reset_index()
        user_counts.columns = ["User", "Edits"]
        st.altair_chart(
            alt.Chart(user_counts).mark_bar().encode(
                x="User:N", y="Edits:Q", color="User:N"
            ).properties(title="Edits by User", width=600, height=300),
            use_container_width=True
        )

    if "Lifecycle Phase" in df.columns:
        lifecycle_counts = df["Lifecycle Phase"].value_counts().reset_index()
        lifecycle_counts.columns = ["Lifecycle Phase", "Count"]
        st.altair_chart(
            alt.Chart(lifecycle_counts).mark_bar().encode(
                x="Lifecycle Phase:N", y="Count:Q", color="Lifecycle Phase:N"
            ).properties(title="Assemblies by Lifecycle Phase", width=600, height=300),
            use_container_width=True
        )

    if "ECO Status" in df.columns:
        eco_counts = df["ECO Status"].value_counts().reset_index()
        eco_counts.columns = ["ECO Status", "Count"]
        st.altair_chart(
            alt.Chart(eco_counts).mark_bar().encode(
                x="ECO Status:N", y="Count:Q", color="ECO Status:N"
            ).properties(title="ECOs by Status", width=600, height=300),
            use_container_width=True
        )

    # Mockup CAD preview image
    st.markdown("### 🧷 CAD File Preview")
    st.image("mock_cad_preview.png", caption="CAD Drawing - Assembly 102-RevB", width=400)

    # Prompt generation
    table_str = df.to_markdown(index=False)
    if prompt_type == "Freeform Prompt":
        custom_input = st.text_area("✍️ Enter your custom prompt (use {table} to insert data)", height=200)
        final_prompt = custom_input.replace("{table}", table_str)
    else:
        final_prompt = templates[prompt_type].replace("{table}", table_str)

    st.subheader("🧠 Generated Prompt")
    st.code(final_prompt, language="markdown")
    st.download_button("📥 Download Prompt", data=final_prompt, file_name="llm_prompt.txt")

# BOM Data Preview
if uploaded_bom is not None:
    st.subheader("📘 BOM Data Preview")
    bom_df = pd.read_csv(uploaded_bom)
    st.dataframe(bom_df.head(100), use_container_width=True)
