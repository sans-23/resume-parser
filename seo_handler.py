import streamlit as st # type: ignore
from datetime import datetime
import os

def get_sitemap_xml():
    """Generate sitemap.xml content"""
    base_url = os.getenv('REPL_SLUG', 'https://ats-resume-analyzer.example.com')
    current_date = datetime.now().strftime('%Y-%m-%d')

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{base_url}</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>
"""

def get_robots_txt():
    """Generate robots.txt content"""
    base_url = os.getenv('REPL_SLUG', 'https://ats-resume-analyzer.example.com')

    return f"""User-agent: *
Allow: /
Sitemap: {base_url}/sitemap.xml
"""

def handle_seo_routes():
    """Handle SEO-related routes"""
    route = st.query_params.get("route", None)

    if route == "sitemap.xml":
        st.markdown(get_sitemap_xml(), unsafe_allow_html=True)
        return True
    elif route == "robots.txt":
        st.markdown(get_robots_txt(), unsafe_allow_html=True)
        return True

    return False