import streamlit as st
import pandas as pd
import os
from collections import Counter

from utils.youtube_utils import extract_video_id, get_comments, get_video_title
from utils.transcript import get_transcript_text, summarize_with_groq
from utils.target_generator import generate_target
from hybrid.pipeline import predict_stance


# ================================
# 🎨 PAGE CONFIG
# ================================
st.set_page_config(
    page_title="YouTube Stance Dashboard",
    page_icon="🎥",
    layout="wide"
)

# ================================
# 🏷️ HEADER
# ================================
st.markdown("""
# 🎥 YouTube Stance Detection Dashboard
Analyze public opinion using NLP + LLMs
""")
st.divider()

# ================================
# 🔗 INPUT SECTION
# ================================
col1, col2 = st.columns([3, 1])

with col1:
    url = st.text_input("🔗 Enter YouTube URL")

with col2:
    order_option = st.selectbox(
        "📊 Comment Type",
        ["Relevance (Top Comments)", "Time (Latest Comments)"]
    )

# ================================
# ▶️ ANALYZE BUTTON
# ================================
if st.button("🚀 Analyze"):

    video_id = extract_video_id(url)

    if not video_id:
        st.error("❌ Invalid URL")
        st.stop()

    # Map UI to API param
    order_type = "relevance" if "Relevance" in order_option else "time"
    st.info(f"📌 Using: {order_type.upper()} comments")

    # ================================
    # 🔍 FETCH COMMENTS
    # ================================
    with st.spinner("🔍 Fetching comments..."):
        comments_data = get_comments(video_id, 50, order_type)

    if not comments_data:
        st.warning("⚠️ No comments found or API timeout")
        st.stop()

    comments = [c["text"] for c in comments_data]

    # ================================
    # 📜 TRANSCRIPT
    # ================================
    with st.spinner("📜 Getting transcript..."):
        transcript = get_transcript_text(video_id)

    title = get_video_title(video_id)

    # ================================
    # 🎯 TARGET EXTRACTION
    # ================================
    st.subheader("🎯 Target Extraction")

    target = None

    if transcript:
        with st.spinner("🧠 Summarizing transcript..."):
            transcript_summary = summarize_with_groq(transcript)

        if transcript_summary:
            st.success("📄 Transcript Summary Generated")
            with st.expander("View Summary"):
                st.write(transcript_summary)

            target = generate_target(transcript_summary, title)
        else:
            st.warning("⚠️ Transcript summarization failed — using comments")

    # Fallback to comments
    if not target or target == "unknown":
        st.info("🧠 Generating target from comments...")
        comments_text = " ".join(comments[:50])
        target = generate_target(comments_text, title)

    if not target or target == "unknown":
        st.error("❌ Unable to generate target")
        st.stop()

    st.success(f"🎯 Final Target: {target}")

    # ================================
    # 🤖 STANCE PREDICTION
    # ================================
    st.subheader("🤖 Stance Prediction")

    progress_bar = st.progress(0, text="Processing comments...")

    stances = []
    total = len(comments)

    for i, comment in enumerate(comments):
        try:
            res = predict_stance(comment, target)

            if isinstance(res, dict):
                stance = res.get("final", "neutral")
            else:
                stance = res

        except:
            stance = "neutral"

        stances.append(stance)

        progress_bar.progress((i + 1) / total, text=f"Processing {i+1}/{total}")

    st.success("✅ Prediction Completed!")

    # ================================
    # 💾 SAVE RESULTS
    # ================================
    results = []

    for comment, stance in zip(comments, stances):
        results.append({
            "youtube_id": video_id,
            "comment": comment,
            "target": target,
            "stance": stance
        })

    df = pd.DataFrame(results)

    file_path = "TVserial.csv"

    df.to_csv(
        file_path,
        mode="a",
        header=not os.path.exists(file_path),
        index=False
    )

    # ================================
    # 📊 DASHBOARD RESULTS
    # ================================
    st.divider()
    st.header("📊 Analysis Dashboard")

    stance_counts = Counter(stances)

    total_comments = len(stances)
    favor = stance_counts.get("favor", 0)
    against = stance_counts.get("against", 0)
    neutral = stance_counts.get("neutral", 0)

    # 🔢 Metrics Cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💬 Total Comments", total_comments)
    col2.metric("👍 Favor", favor)
    col3.metric("👎 Against", against)
    col4.metric("😐 Neutral", neutral)

    # ================================
    # 📈 CHARTS
    # ================================
    st.subheader("📊 Stance Analysis")

    chart_col1, chart_col2 = st.columns(2)

    chart_data = pd.DataFrame({
        "Stance": list(stance_counts.keys()),
        "Count": list(stance_counts.values())
    })

    with chart_col1:
        st.write("### 📊 Count Distribution")
        st.bar_chart(chart_data.set_index("Stance"))

    with chart_col2:
        st.write("### 🥧 Percentage Share")
        st.plotly_chart(
            {
                "data": [{
                    "labels": chart_data["Stance"],
                    "values": chart_data["Count"],
                    "type": "pie"
                }],
                "layout": {"height": 400}
            }
        )

    # ================================
    # 📢 INSIGHTS
    # ================================
    st.subheader("📢 Insights")

    dominant = max(stance_counts, key=stance_counts.get)

    if dominant == "favor":
        st.success("📈 Audience sentiment is mostly POSITIVE.")
    elif dominant == "against":
        st.error("📉 Audience sentiment is mostly NEGATIVE.")
    else:
        st.warning("⚖️ Audience sentiment is mostly NEUTRAL.")

    # ================================
    # 🎬 VIDEO INFO
    # ================================
    st.subheader("🎬 Video Details")

    info_col1, info_col2 = st.columns(2)

    with info_col1:
        st.write("**Title:**", title)

    with info_col2:
        st.write("**Target:**", target)

    # ================================
    # 🔍 SAMPLE RESULTS
    # ================================
    with st.expander("🔍 View Sample Predictions"):
        st.dataframe(pd.DataFrame(results[:10]), use_container_width=True)

    # ================================
    # ⬇️ DOWNLOAD
    # ================================
    st.download_button(
        label="⬇️ Download Results CSV",
        data=df.to_csv(index=False),
        file_name="stance_results.csv",
        mime="text/csv"
    )

    st.success(f"✅ Results saved to {file_path}")