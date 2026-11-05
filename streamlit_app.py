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

T2_MARKERS = {"pt_activity", "hs_crp", "potassium", "aptt"}
T1_MARKERS = {"urine_ketone", "basophil_pct", "urine_sg"}


def show_result(df, res, tier):
    res = res.copy()
    res.insert(0, "tier", tier)
    if "case_id" in df.columns:
        res.insert(1, "case_id", df["case_id"].astype(str).values)
    show_cols = [c for c in ["tier", "case_id", "calibrated_score", "high_risk", "near_threshold"] if c in res.columns]
    st.success(f"当前评分：{tier}。请核对 tier 和 case_id 后再抄分。")
    st.dataframe(res[show_cols], use_container_width=True, hide_index=True)
    with st.expander("查看完整输出（含输入列）"):
        full = pd.concat([df.reset_index(drop=True), res.drop(columns=["tier", "case_id"], errors="ignore")], axis=1)
        st.dataframe(full, use_container_width=True)
        st.download_button(f"Download {tier} scores", full.to_csv(index=False).encode("utf-8-sig"), f"{tier.lower()}_scores.csv")


tab1, tab2 = st.tabs(["T1 pre-screen", "T2 specialist priority"])

with tab1:
    st.header("T1 pre-screen")
    st.caption("只上传 V1_T1.csv / V2_T1.csv / V3_T1.csv / V4_T1.csv。不要在这里上传 T2 文件。")
    f1 = st.file_uploader("Upload T1 CSV", type="csv", key="t1")
    if f1 is not None:
        df = pd.read_csv(f1)
        if (T2_MARKERS & set(df.columns)) and not (T1_MARKERS & set(df.columns)):
            st.error("这看起来是 T2 文件。请切换到上方的 **T2 specialist priority** 标签再上传。")
        elif not (T1_MARKERS & set(df.columns)):
            st.error("没有找到 T1 必需列（例如 urine_ketone、basophil_pct）。请用 case_csvs 里的 V*_T1.csv 原文件。")
        else:
            show_result(df, score_t1(df), "T1")

with tab2:
    st.header("T2 specialist priority")
    st.caption("只上传 V1_T2.csv / V2_T2.csv / V3_T2.csv / V4_T2.csv。不要在这里上传 T1 文件。")
    f2 = st.file_uploader("Upload T2 CSV", type="csv", key="t2")
    if f2 is not None:
        df = pd.read_csv(f2)
        if (T1_MARKERS & set(df.columns)) and not (T2_MARKERS & set(df.columns)):
            st.error("这看起来是 T1 文件。请切换到上方的 **T1 pre-screen** 标签再上传。")
        elif not (T2_MARKERS & set(df.columns)):
            st.error("没有找到 T2 必需列（例如 pt_activity、hs_crp）。请用 case_csvs 里的 V*_T2.csv 原文件。")
        else:
            show_result(df, score_t2(df), "T2")
