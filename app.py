import streamlit as st
from utils.data_lineage import analyze_lineage
from utils.quality import run_data_quality
from utils.llama_helper import ask_llama

# App Title
st.set_page_config(page_title="Data Lineage & Quality Checker", layout="wide")
st.title("🧮 Data Lineage & Quality Checker")
st.markdown("---")

# Sidebar Navigation
menu = st.sidebar.radio("Select Option", ["Data Lineage", "Data Quality", "AI Assistant"])

# 1️⃣ Data Lineage
if menu == "Data Lineage":
    st.header("🌳 Interactive Data Lineage Tree (Optimized)")
    st.caption("Explore how data moves from **source → transformed → target**")

    if st.button("Run Lineage Analysis"):
        with st.spinner("Analyzing lineage... (cached for speed)"):
            lineage_tree = analyze_lineage()

        st.success("✅ Lineage Analysis Complete! (Loaded instantly next time)")

        def render_tree(tree, level=0):
            for source_col, transforms in tree.items():
                with st.expander(f"📦 Source: `{source_col}`", expanded=(level == 0)):
                    for transform_col, targets in transforms.items():
                        with st.expander(f"🔸 Transformed: `{transform_col}`"):
                            for target_col in targets:
                                st.markdown(f"- 🎯 Target: **`{target_col}`**")

        render_tree(lineage_tree)

# 2️⃣ Data Quality
if menu == "Data Quality":
    st.header("🧩 Data Quality Dashboard")

    if st.button("Run Quality Checks"):
        with st.spinner("Running all checks..."):
            results = run_data_quality()

        if not results:
            st.stop()

        # --- Completeness ---
        st.subheader("✅ Completeness Check")
        st.pyplot(results["completeness_fig"])
        st.dataframe(results["completeness"])

        # --- Uniqueness ---
        st.subheader("🧠 Uniqueness Check")
        st.pyplot(results["uniqueness_fig"])
        st.dataframe(results["uniqueness"])

        # --- Duplicate Rows ---
        st.subheader("🧍‍♂️ Duplicate Rows (All Columns)")
        if len(results["duplicates"]) > 0:
            st.warning(f"{len(results['duplicates'])} duplicate rows found!")
            st.dataframe(results["duplicates"])
        else:
            st.success("No duplicate rows found.")

        # --- Date-based Duplicates ---
        st.subheader("📅 Duplicate Rows by Date")
        st.info(results["date_message"])
        if not results["date_duplicates"].empty:
            st.dataframe(results["date_duplicates"])

        # --- Version Comparison ---
        st.subheader("🔍 Version Comparison")
        comp = results["comparison"]
        st.write("📈 Added Rows:", len(comp["Added Rows"]))
        st.write("📉 Removed Rows:", len(comp["Removed Rows"]))
        with st.expander("Show Added Rows"):
            st.dataframe(comp["Added Rows"])
        with st.expander("Show Removed Rows"):
            st.dataframe(comp["Removed Rows"])

# 3️⃣ AI Assistant
elif menu == "AI Assistant":
    st.header("💬 AI Assistant (Explain Your Results)")
    prompt = st.text_area("Enter your question or description:")

    if st.button("Ask AI"):
        if prompt.strip():
            with st.spinner("Thinking..."):
                response = ask_llama(prompt)
            st.success("AI Response:")
            st.write(response)
        else:
            st.warning("Please enter a prompt before asking the AI.")