import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated, Optional
import os
from dotenv import load_dotenv
import zipfile
import io
import fitz  
import pandas as pd
import time

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("gemini")

st.set_page_config(page_title="AI Resume Analyzer", page_icon="🤖")
st.title("AI-Powered Resume Analyzer")

uploaded_zip = st.file_uploader(
    "Upload ZIP file containing PDF resumes",
    type=["zip"]
)

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

class DataFormat(TypedDict):
    summary: Annotated[str, "Short professional summary"]
    experience: Annotated[Optional[int], "Years of experience or null"]
    skills: list[str]

structured_model = model.with_structured_output(DataFormat)

results = []

# -------------------- PROCESS ZIP --------------------
if uploaded_zip is not None:

    extract_dir = "resumes_extracted"
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(io.BytesIO(uploaded_zip.read())) as zip_ref:
        files = [f for f in zip_ref.namelist() if f.lower().endswith(".pdf")]
        zip_ref.extractall(extract_dir)

    st.success(f"Extracted {len(files)} PDF resumes")

    # -------------------- PROCESS EACH PDF --------------------
    for idx, file in enumerate(files):

        pdf_path = os.path.join(extract_dir, file)

        # ---------- TEXT EXTRACTION ----------
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()

        if not text.strip():
            st.warning(f"⚠ No text found in {file}")
            continue

        st.markdown(f"### 📄 {file}")
        st.text_area(
            "Extracted Text",
            text,
            height=250,
            key=f"text_{idx}"   # ✅ UNIQUE KEY FIX
        )

        # ---------- LLM CALL (SAFE) ----------
        try:
            response = structured_model.invoke(
                f"""
                Extract the following from the resume:
                - summary
                - experience (number of years or null)
                - skills (list)

                Resume Text:
                {text}
                """
            )

            results.append({
                "file_name": file,
                "summary": response.get("summary", ""),
                "experience": response.get("experience"),
                "skills": ", ".join(response.get("skills", []))
            })

            time.sleep(1.2)  # ✅ RATE LIMIT PROTECTION

        except Exception as e:
            st.error(f"LLM failed for {file}: {e}")
            continue

# -------------------- CSV DOWNLOAD --------------------
if results:
    df = pd.DataFrame(results)
    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label=" Download Resume Analysis CSV",
        data=csv_data,
        file_name="resume_analysis.csv",
        mime="text/csv"
    )
