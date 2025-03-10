import streamlit as st # type: ignore
import os
from ai import get_ai_response
from parse_job_description import parse_job_description
from resume_analyzer import ResumeAnalyzer
from text_extractor import PDFTextExtractor
from utils import load_default_keywords, load_default_sections
import tempfile
from seo_handler import handle_seo_routes
from io import BytesIO

# SEO Configuration
st.set_page_config(
    page_title="ATS Resume Analyzer & Optimizer | Free Resume Scanner",
    page_icon="📄",
    layout="wide",
    menu_items={
        'Get Help': 'https://github.com/yourusername/ats-resume-analyzer',
        'Report a bug': "https://github.com/yourusername/ats-resume-analyzer/issues",
        'About': """
        # ATS Resume Analyzer
        Optimize your resume for Applicant Tracking Systems (ATS) with our free tool.
        Get instant feedback on ATS compatibility, keyword optimization, and formatting.
        """
    }
)

def inject_seo_metadata():
    """Inject SEO metadata including schema.org JSON-LD"""
    st.markdown("""
        <head>
            <meta name="description" content="Free ATS resume analyzer tool. Check your resume's ATS compatibility, get instant feedback, keyword suggestions, and formatting recommendations.">
            <meta name="keywords" content="ATS resume analyzer, resume scanner, ATS compatibility checker, resume optimizer, job application, career tools">
        </head>
    """, unsafe_allow_html=True)

    # Inject Schema.org JSON-LD using a hidden div
    schema_markup = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "ATS Resume Analyzer",
        "description": "Free tool to analyze resume compatibility with Applicant Tracking Systems",
        "applicationCategory": "Career Tool",
        "operatingSystem": "All",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        }
    }

    st.markdown(f"""
        <script type="application/ld+json">
        {str(schema_markup).replace("'", '"')}
        </script>
        <div style="display: none">Schema.org metadata for search engines</div>
    """, unsafe_allow_html=True)


def analyze_resume(job_description, uploaded_file):
    with st.spinner("Analyzing your resume..."):
            try:
                # Extract text
                job_description=parse_job_description(job_description)
                with st.expander('View Job Description', expanded=True):
                    st.markdown(f"{job_description['content']}")
                pdf_bytes = uploaded_file.getvalue()
                pdf_file = BytesIO(pdf_bytes)
                extractor = PDFTextExtractor()
                extracted_text = extractor.extract_text(pdf_file)

                if len(extracted_text) < 50:
                    st.error("The uploaded PDF appears to be image-based or contains very little text. Please upload a text-based PDF.")
                    return

                # Initialize analyzer
                analyzer = ResumeAnalyzer(
                    text=extracted_text,
                    sections=load_default_sections(),
                    keywords=load_default_keywords()
                )

                # Perform analysis
                results = analyzer.analyze()

                # Display results in SEO-friendly structure
                col1, col2 = st.columns(2)

                with col1:
                    st.header("📊 ATS Compatibility Score")
                    st.markdown(f"### {results['total_score']}/100")

                    st.subheader("Detailed Score Breakdown")
                    st.markdown(f"- **Resume Sections**: {results['section_score']}/30")
                    st.markdown(f"- **Industry Keywords**: {results['keyword_score']}/30")
                    st.markdown(f"- **Contact Details**: {results['contact_score']}/20")
                    st.markdown(f"- **Resume Format**: {results['format_score']}/20")

                with col2:
                    st.header("📋 Detailed Analysis")
                    st.markdown("### ✓ Detected Sections")
                    for section in results['sections_found']:
                        st.write(f"- {section}")

                    st.markdown("### ✓ Matched Keywords")
                    for keyword in results['keywords_found']:
                        st.write(f"- {keyword}")

                    st.markdown("### Contact Information")
                    contact_info = results['contact_info']
                    if contact_info.get('name'):
                        st.write(f"- Name: {contact_info['name']}")
                    if contact_info.get('email'):
                        st.write(f"- Email: {contact_info['email']}")
                    if contact_info.get('phone'):
                        st.write(f"- Phone: {contact_info['phone']}")
                    if contact_info.get('linkedin'):
                        st.write(f"- LinkedIn: {contact_info['linkedin']}")
                    if contact_info.get('github'):
                        st.write(f"- GitHub: {contact_info['github']}")

                    st.markdown("### Format Analysis")
                    formatting = results['formatting_details']
                    st.write(f"- 📄 Pages: {formatting['estimated_pages']:.1f}")
                    st.write(f"- • Bullet Points Ratio: {formatting['bullet_point_ratio']:.2f}")
                    st.write(f"- ↔️ Line Length: {formatting['avg_line_length']:.1f} words")

                st.header("🤖 AI-Powered Recommendations")
                with st.spinner("Generating smart recommendations..."):
                    recommendations = analyzer.get_ai_recommendations()
                    print(recommendations)
                    st.markdown(recommendations)

                # Add social sharing buttons
                st.markdown("""
                    ### 📱 Share this tool
                    Help others optimize their resumes by sharing:
                    - [Share on LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https://your-app-url)
                    - [Share on Twitter](https://twitter.com/intent/tweet?text=Check%20out%20this%20free%20ATS%20Resume%20Analyzer!&url=https://your-app-url)
                """)

                st.session_state.analysis_complete = True

            except Exception as e:
                st.error(f"An error occurred while analyzing the resume: {str(e)}")


def main():
    # Handle SEO routes first
    if handle_seo_routes():
        return

    # Inject SEO metadata
    inject_seo_metadata()

    st.title("📄 ATS Resume Analyzer")

    # SEO-optimized content structure
    st.markdown("""
    ### Optimize Your Resume for ATS Systems
    Upload your resume to get instant feedback on:
    - ATS Compatibility Score
    - Keyword Analysis
    - Section Organization
    - Formatting Recommendations
    """)

    # Add informative section about ATS
    with st.expander("What is ATS? 🤔"):
        st.markdown("""
        An Applicant Tracking System (ATS) is software used by employers to:
        - Screen job applications
        - Parse resumes
        - Track candidates

        Our tool helps ensure your resume is optimized for these systems.
        """)

    # Initialize session state
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False

    # upload_job_description_and_resume()

    # File upload
    job_description = st.text_area('Job Description')
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF format)", 
        type=['pdf'],
        help="For best results, upload a text-based PDF file"
    )

    if st.button('Submit'):
        if job_description and uploaded_file:
            st.success('Job description and resume uploaded successfully!')
            st.write('Uploaded File:', uploaded_file.name)
            analyze_resume(job_description, uploaded_file)
        else:
            st.error('Please fill in both fields.')

    

    # Add SEO-friendly footer content
    st.markdown("""
    ---
    ### Why Use Our ATS Resume Analyzer?
    - ✅ **100% Free** - No hidden costs or premium features
    - 🔒 **Private & Secure** - We don't store your resume
    - 🎯 **Accurate Analysis** - Based on real ATS systems
    - 💡 **Smart Recommendations** - Powered by AI
    - ⚡ **Instant Results** - Get feedback in seconds
    """)

if __name__ == "__main__":
    main()