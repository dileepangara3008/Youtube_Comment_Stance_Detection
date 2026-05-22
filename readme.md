# 📌 YouTube Comment Stance Detection System

A Hybrid Natural Language Inference (NLI) and Large Language Model (LLM) Pipeline for automated public opinion analysis on YouTube comments.

---

## 🚀 Overview

This project presents a fully automated system that analyzes YouTube comments and classifies them into:

- 👍 Favor  
- 👎 Against  
- 😐 Neutral  

Unlike traditional sentiment analysis, this system performs **target-based stance detection**, identifying whether a comment supports or opposes a specific topic.

---

## 🧠 Key Features

- 🔗 Input: YouTube URL  
- 💬 Automatic comment extraction (YouTube API)  
- 📄 Transcript summarization using LLM  
- 🎯 Automatic target extraction  
- ⚡ Hybrid stance classification (NLI + LLM)  
- 📊 Interactive Streamlit dashboard  
- 📁 CSV export  

---

## 🏗️ System Architecture
YouTube URL
↓
Video ID Extraction
↓
Comment Retrieval (YouTube API)
↓
Transcript Retrieval + Summarization
↓
Target Extraction (LLM)
↓
Hybrid Stance Classification (NLI + LLM)
↓
Dashboard + CSV Export


---

## ⚙️ Tech Stack

- **Language:** Python 3.10+  
- **Models:**
  - facebook/bart-large-mnli (NLI)
  - Llama-3.1-8b-instant (LLM via Groq API)  
- **Libraries:**
  - Hugging Face Transformers  
  - Streamlit  
  - Pandas  
- **APIs:**
  - YouTube Data API v3  
  - Groq API  
- **Others:**
  - youtube-transcript-api  

---

## 📊 Dataset Collection

- Data collected dynamically using YouTube Data API v3  
- No pre-built dataset used  
- Includes:
  - Comment text  
  - Like counts  
  - Video metadata  

---

## 📈 Dataset Statistics

| Metric | Value |
|------|------|
| Total Videos | 15 |
| Total Comments | 900 |
| Avg Comments/Video | 60 |
| Domains Covered | 6 |
| Target Extraction Accuracy | 87% |

---

## 📊 Stance Distribution

| Stance | Count | Percentage |
|-------|------|-----------|
| Neutral | 388 | 43.1% |
| Against | 327 | 36.3% |
| Favor | 185 | 20.6% |

---

## 🧪 Model Approach

### 🔹 NLI-Based Classification
- Uses BART-MNLI  
- Converts stance detection into hypothesis testing  

### 🔹 LLM-Based Classification
- Uses Llama 3  
- Handles sarcasm, implicit meaning, and context  

### 🔹 Hybrid Fusion Strategy
- If both models agree → accept result  
- If disagreement → prefer LLM output  

---

## ⚠️ Fine-Tuned Model Attempt (DeBERTa)

A DeBERTa model was fine-tuned on the VAST dataset. However:

- Model predicted mostly **neutral**  
- Reasons:
  - Class imbalance  
  - Domain mismatch (VAST vs YouTube comments)  

👉 Therefore, a hybrid zero-shot approach was adopted.

---

## 📊 Results & Observations

- Neutral is the dominant class  
- Against > Favor → reflects negativity bias  
- Domain insights:
  - Politics → Mostly Against  
  - Technology → Mixed  
  - Education → Mostly Neutral  

---

## 🧠 Sarcasm Handling Example
Input: "Yeah great job ruining everything"
Topic: Government policy

NLI → Favor ❌
LLM → Against ✅
Final → Against ✅


---

## 📌 Advantages

- Fully automated pipeline  
- No labeled training data required  
- Handles noisy real-world data  
- Works across multiple domains  

---

## ⚠️ Limitations

- Dependent on external APIs  
- No supervised fine-tuning for YouTube data  
- Limited multilingual support  

---

## 🔮 Future Work

- Multilingual stance detection  
- Sarcasm-aware preprocessing  
- Multi-target analysis  
- Fine-tuned stance models  
- Engagement-weighted analysis  
- Scalable deployment  

---

## 🖥️ How to Run

```bash
# Clone repository
git clone <your-repo-link>

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py

👨‍💻 Authors
Dileep Angara

📄 License

This project is developed for academic purposes.

⭐ Final Note

This project demonstrates a real-world NLP system combining classical machine learning (NLI) with modern LLMs, achieving effective stance detection without task-specific training data.