import pandas as pd
import streamlit as st

from demo_predict import score_t1, score_t2

st.set_page_config(page_title="ACCORD-SL T1/T2 research demo", layout="wide")
st.title("ACCORD-SL T1/T2 research demonstration")
st.warning(
    "Research use only. Not a diagnosis; not for clinical use. "
    "This public demo uses a transparent linear approximation of the locked models; "
    "scores are for workflow evaluation only and are not the manuscript's full-model outputs."
)

tab1, tab2 = st.tabs(["T1 pre-screen", "T2 specialist priority"])

with tab1:
    st.subheader("T1: 20 items + age")
    f1 = st.file_uploader("Upload T1 CSV", type="csv", key="t1")
    if f1 is not None:
        df = pd.read_csv(f1)
        out = pd.concat([df.reset_index(drop=True), score_t1(df)], axis=1)
        st.dataframe(out, use_container_width=True)
        st.download_button("Download T1 scores", out.to_csv(index=False).encode("utf-8-sig"), "t1_scores.csv")

with tab2:
    st.subheader("T2: 11 items + age")
    f2 = st.file_uploader("Upload T2 CSV", type="csv", key="t2")
    if f2 is not None:
        df = pd.read_csv(f2)
        out = pd.concat([df.reset_index(drop=True), score_t2(df)], axis=1)
        st.dataframe(out, use_container_width=True)
        st.download_button("Download T2 scores", out.to_csv(index=False).encode("utf-8-sig"), "t2_scores.csv")
