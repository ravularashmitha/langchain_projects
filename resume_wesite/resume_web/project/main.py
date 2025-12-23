import os, zipfile, streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from PyPDF2 import PdfReader
from docx import Document

## Load .env (API Key)
load_dotenv() 
os.environ["GOOGLE_API_KEY"] = os.getenv("Gemini")

## ---------------- User Interface ----------------
st.set_page_config("AI Portfolio Generator", "🤖", layout="centered")

## Title & Subtitle 
st.markdown("<h1 style='text-align:center;font-family:Inter,Poppins,sans-serif;"
            "font-size:46px;font-weight:800;color:#1F2937;'>ResumeCraft <span style='color:#6366F1;'>"
            "AI</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;font-family:Inter,sans-serif;"
            "font-size:18px;color:#6B7280;margin-top:-8px;'>"
            "Transform your resume into a professional portfolio website</p>", unsafe_allow_html=True)
## Space
st.markdown("<div style='height:50px'></div>", unsafe_allow_html=True)

## ---------------- Resume Upload ----------------
uploaded_file = st.file_uploader("📄 Upload Resume Document", type=["pdf", "docx"],
                                 help="Accepted file formats: PDF, DOCX")

## Space
st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
## Footer
Footer = """
<p style='text-align:center;font-family:Inter,sans-serif;
font-size:14px;color:#6B7280;margin-top:40px;'>
© 2025 ResumeCraft AI · Built with Streamlit & Gemini
</p>
"""
if not uploaded_file:
    st.markdown(Footer, unsafe_allow_html=True)
    st.stop()

## Resume Extraction 
def extract_resume(file):
    if file.type == "application/pdf":
        return " ".join(p.extract_text() or "" for p in PdfReader(file).pages)
    return " ".join(p.text for p in Document(file).paragraphs)

resume_text = extract_resume(uploaded_file)

if not resume_text.strip():
    st.error("Failed to extract resume text")
    st.markdown(Footer, unsafe_allow_html=True)
    st.stop()
    
## Model 
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

# ---------------- LLM #1: Resume → Website Prompt ----------------
profile_prompt = f"""
You are a resume analyzer.
Extract the following details from the resume text:
Name, Skills, Experience, Projects, Education, Achievements.

Resume Text: 
{resume_text}
Return the information in a clean structured format.
"""
profile = model.invoke([("user", profile_prompt)]).content

# ---------------- LLM #2: Prompt → Website Code ----------------
website_prompt = f"""
You are an expert frontend developer. Using the structured resume data below, generate a professional portfolio website.

{profile}

Return ONLY code in this exact format:

--html--
[HTML]
--html--

--css--
[CSS]
--css--

--js--
[JS]
--js--
"""
content = model.invoke([("user", website_prompt)]).content

## Safe extraction
def block(tag):
    if tag in content:
        return content.split(tag)[1].split(tag)[0].strip()
    return ""

html, css, js = block("--html--"), block("--css--"), block("--js--")

if not html or not css:
    st.error("Website generation failed. Try again.")
    st.markdown(Footer, unsafe_allow_html=True)
    st.stop()

# ---------------- Save & ZIP ----------------
files = {"index.html": html, "style.css": css, "script.js": js}
for name, data in files.items():
    with open(name, "w", encoding="utf-8") as f:
        f.write(data)

with zipfile.ZipFile("portfolio_website.zip", "w") as z:
    for f in files:
        z.write(f)

## Download
with open("portfolio_website.zip", "rb") as f:
    st.download_button("⬇ Download Portfolio Website", f.read(), "portfolio_website.zip")

st.success("Portfolio website generated successfully!")

## Footer   
st.markdown(Footer, unsafe_allow_html=True)
