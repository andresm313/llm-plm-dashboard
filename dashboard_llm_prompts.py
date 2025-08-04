
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="LLM Prompt Generator from CSV", layout="wide")
st.title("📊 LLM Prompt Generator from CSV")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

templates = {
    "Summarize Performance": "Here is a dataset:\n\n{table}\n\nPlease summarize key performance metrics and anomalies.",
    "Root Cause Analysis": "Given this MES data:\n\n{table}\n\nIdentify potential root causes of alerts or deviations.",
    "Suggest Improvements": "Here is a dataset:\n\n{table}\n\nIdentify areas of improvement and propose 2 concrete suggestions.",
    "Freeform Prompt": "{custom}"
}

st.sidebar.header("Select Prompt Type")
prompt_type = st.sidebar.selectbox("Prompt Style", list(templates.keys()))

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Preview Data")
    st.dataframe(df.head(100), use_container_width=True)

    # --------- Visualizations ----------
    st.markdown("## 📈 Visualizations")

    if "Temp Avg (°C)" in df.columns:
        if "Line" in df.columns:
            st.markdown("### Average Temperature by Line")
            temp_chart = alt.Chart(df).mark_line(point=True).encode(
                x=alt.X("Start Time:N", title="Time"),
                y=alt.Y("Temp Avg (°C):Q"),
                color="Line:N"
            ).properties(width=600, height=300)
            st.altair_chart(temp_chart, use_container_width=True)

        elif "Timestamp" in df.columns:
            st.markdown("### Temperature Over Time")
            time_chart = alt.Chart(df).mark_line(point=True).encode(
                x="Timestamp:N",
                y="Temp Avg (°C):Q",
                color="Line:N"
            ).properties(width=600, height=300)
            st.altair_chart(time_chart, use_container_width=True)

    if "Alerts" in df.columns:
        st.markdown("### Alert Types")
        alert_counts = df["Alerts"].value_counts().reset_index()
        alert_counts.columns = ["Alert Type", "Count"]
        bar_chart = alt.Chart(alert_counts).mark_bar().encode(
            x="Alert Type:N",
            y="Count:Q",
            color="Alert Type:N"
        ).properties(width=600, height=300)
        st.altair_chart(bar_chart, use_container_width=True)

    # --------- Prompt Generation ----------
    table_str = df.to_markdown(index=False)

    if prompt_type == "Freeform Prompt":
        custom_input = st.text_area("Enter your custom prompt (use {table} to insert data)", height=200)
        final_prompt = custom_input.replace("{table}", table_str)
    else:
        final_prompt = templates[prompt_type].replace("{table}", table_str)

    st.subheader("🧠 Generated Prompt")
    st.code(final_prompt, language="markdown")
    st.download_button("Download Prompt as .txt", data=final_prompt, file_name="llm_prompt.txt")
