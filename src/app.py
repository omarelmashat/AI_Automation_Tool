from pathlib import Path

import pandas as pd
import streamlit as st

from reader import MAX_CHARS
from classifier import classify
from organizer import unique_destination, write_log

ROOT = Path(__file__).resolve().parent.parent
ORGANIZED = ROOT / "organized"
LOG = ROOT / "log.csv"

def process_upload(uploaded) -> dict:
    try:
        text = uploaded.getvalue().decode("utf-8", errors="ignore").strip()[:MAX_CHARS]
        result = classify(text)

        folder = ORGANIZED / result["category"]
        folder.mkdir(parents=True, exist_ok=True)
        unique_destination(folder, uploaded.name).write_bytes(uploaded.getvalue())

        write_log(LOG, uploaded.name, result["category"], result["summary"], "ok")
        return {"File": uploaded.name, "Category": result["category"],
                "Summary": result["summary"], "Status": "ok"}
    except Exception as e:
        write_log(LOG, uploaded.name, "", "", f"error: {e}")
        return {"File": uploaded.name, "Category": "-",
                "Summary": "", "Status": f"error: {e}"}

st.set_page_config(page_title="Smart Folder Organizer", page_icon="🗂️")

st.title("🗂️ Smart Folder Organizer")
st.caption("Upload text files. The AI classifies and summarizes each one, then files it into a category folder.")

uploaded_files = st.file_uploader(
    "Upload .txt or .md files", type=["txt", "md"], accept_multiple_files=True
)

if st.button("Classify and organize", type="primary", disabled=not uploaded_files):
    rows = []
    progress = st.progress(0)
    for i, f in enumerate(uploaded_files, start=1):
        rows.append(process_upload(f))
        progress.progress(i / len(uploaded_files))
    st.session_state["rows"] = rows

if "rows" in st.session_state:
    df = pd.DataFrame(st.session_state["rows"])

    ok = df[df["Status"] == "ok"]
    st.success(f"Processed {len(df)} file(s): {len(ok)} succeeded, {len(df) - len(ok)} failed.")

    if not ok.empty:
        st.subheader("Files per category")
        st.bar_chart(ok["Category"].value_counts())

    st.subheader("Results")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.download_button(
        "Download results as CSV",
        data=df.to_csv(index=False),
        file_name="results.csv",
        mime="text/csv",
    )

