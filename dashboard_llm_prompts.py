import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="PLM Prompt Generator", layout="wide")
st.title("🧠 PLM Prompt Generator with LLM Integration")

uploaded_file = st.file_uploader("Upload a PLM-related CSV file", type=["csv"])

templates = {
    "Summarize Product Overview": "Here is a dataset:\n\n{table}\n\nPlease summarize the status of BOMs, revisions, and lifecycle stages.",
    "Change Impact Analysis": "Given this PLM change data:\n\n{table}\n\nIdentify high-impact ECOs and summarize pending approvals or bottlenecks.",
    "Collaboration Summary": "Review the following activity data:\n\n{table}\n\nSummarize recent actions, outstanding approvals, and collaboration gaps.",
    "Freeform Prompt": "{custom}"
}

st.sidebar.header("Select Prompt Type")
prompt_type = st.sidebar.selectbox("Prompt Style", list(templates.keys()))

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Data Preview")
    st.dataframe(df.head(100), use_container_width=True)

    # --------- Visualizations ----------
    st.markdown("## 📈 PLM Visual Insights")

    # BOM completeness
    if "BOM Status" in df.columns and "Assembly" in df.columns:
        st.markdown("### BOM Completeness by Assembly")
        bom_chart = alt.Chart(df).mark_bar().encode(
            x=alt.X("Assembly:N", title="Assembly"),
            y=alt.Y("BOM Status:Q", title="Completeness %"),
            color="Assembly:N"
        ).properties(width=700, height=300)
        st.altair_chart(bom_chart, use_container_width=True)

    # ECO status
    if "ECO Status" in df.columns:
        st.markdown("### ECO Status Distribution")
        eco_status = df["ECO Status"].value_counts().reset_index()
        eco_status.columns = ["Status", "Count"]
        eco_chart = alt.Chart(eco_status).mark_bar().encode(
            x="Status:N",
            y="Count:Q",
            color="Status:N"
        ).properties(width=600, height=300)
        st.altair_chart(eco_chart, use_container_width=True)

    # Activity feed
    if "User" in df.columns and "Action" in df.columns:
        st.markdown("### Recent Activity Feed")
        st.dataframe(df[["User", "Action", "Timestamp"]].sort_values("Timestamp", ascending=False).head(10))

    # CAD file preview (mock)
    if "CAD Preview" in df.columns:
        st.markdown("### CAD File Preview")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/3D_CAD_model.png/640px-3D_CAD_model.png", caption="Example CAD Model", use_column_width=True)

    # --------- Prompt Generation ----------
    table_str = df.to_markdown(index=False)

    if prompt_type == "Freeform Prompt":
        custom_input = st.text_area("Enter your custom prompt (use {table} to insert data)", height=200)
        final_prompt = custom_input.replace("{table}", table_str)
    else:
        final_prompt = templates[prompt_type].replace("{table}", table_str)

    st.subheader("🤖 Generated Prompt")
    st.code(final_prompt, language="markdown")
    st.download_button("Download Prompt as .txt", data=final_prompt, file_name="plm_prompt.txt")
