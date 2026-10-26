import streamlit as st
import subprocess

st.set_page_config(page_title="Legal Document Analyzer", page_icon="⚖️")
st.title("⚖️ Automated Legal Document Analyzer")
st.write("Analyze legal documents using Ollama and Llama 3.2.")

document = st.text_area("Paste your legal document", height=250)

if st.button("Analyze Document", type="primary"):
    if not document.strip():
        st.warning("Please paste a document first.")
    else:
        prompt = f"""
You are a legal document analysis assistant.
Use ONLY information in the document. Never invent facts.
For missing information, write "Not specified in the document."

Analyze using these headings:
1. Document Type
2. Parties Involved
3. Purpose
4. Duration
5. Key Obligations
6. Payment Terms
7. Termination Conditions
8. Important Dates
9. Important Clauses: Confidentiality, Liability,
   Intellectual Property and Dispute Resolution
10. Concise Summary

Document:
{document}
"""
        with st.spinner("Analyzing with Llama 3.2..."):
            try:
                result = subprocess.run(
                    ["ollama", "run", "llama3.2", prompt],
                    capture_output=True, text=True, timeout=300
                )
                if result.returncode == 0:
                    st.session_state["analysis"] = result.stdout.strip()
                else:
                    st.error(result.stderr or "Ollama returned an error.")
            except FileNotFoundError:
                st.error("Ollama is not installed or is not available in PATH.")
            except subprocess.TimeoutExpired:
                st.error("Analysis timed out. Try a shorter document.")

if st.session_state.get("analysis"):
    st.subheader("Legal Document Analysis")
    st.markdown(st.session_state["analysis"])
    st.download_button(
        "Download Analysis",
        st.session_state["analysis"],
        file_name="legal_analysis.txt",
        mime="text/plain"
    )

st.caption("Educational use only. AI analysis is not a substitute for advice from a qualified lawyer.")
