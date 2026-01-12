import streamlit as st
import requests
import subprocess
import sys
import os

st.set_page_config(page_title="Agentic PPT Generator", layout="centered")

st.markdown("""
<style>
    .title {font-size: 38px; font-weight: bold; text-align: center; color: #0073e6;}
    .subtext {font-size: 16px; text-align: center; color: grey;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🤖 Agentic PowerPoint Generator</div>", unsafe_allow_html=True)
#st.markdown("<div class='subtext'>Enter details | AI creates PPT | Download instantly</div>", unsafe_allow_html=True)
st.write("")

prompt = st.text_area("📌 Enter PPT Details Here:", height=300,
                      placeholder="enter the prompt")

generate = st.button("🚀 Generate PowerPoint")

output_file_path = "data.pptx"

if generate:
    if not prompt.strip():
        st.error("❌ Please enter valid prompt details.")
    else:
        with st.spinner("⏳ AI is creating your PPT… Please wait!"):
            try:
                res = requests.post(
                    url="https://alexa07.app.n8n.cloud/webhook-test/d5bf190e-4539-4714-a337-fb9cac4b550c",
                    json={"prompt": prompt}
                )

                if res.status_code == 200:
                    st.success("Script generated successfully!")

                    code = res.json()["output"]
                    code = code.replace("```python", "").replace("```", "").strip()

                    with open("ppt_gen.py", "w", encoding="utf-8") as file:
                        file.write(code)

                    subprocess.run([sys.executable, "ppt_gen.py"])

                    if os.path.exists(output_file_path):
                        st.success("🎯 PPT Generated Successfully!")
                    else:
                        st.error("⚠ Script ran but PPT not found!")

                else:
                    st.error(f"❌ Error: {res.status_code}")

            except Exception as e:
                st.error(f"⚠ Something went wrong: {e}")

if os.path.exists(output_file_path):
    with open(output_file_path, "rb") as f:
        st.download_button(
            label="⬇️ Download Your PPT",
            data=f,
            file_name="Generated_Presentation.pptx",
        )

