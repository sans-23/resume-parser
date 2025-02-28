import re
from typing import Dict, List, Optional
import requests # type: ignore

from ai import get_ai_response # type: ignore

class ResumeAnalyzer:
    def __init__(self, text, sections, keywords):
        self.text = text
        self.standard_sections = sections
        self.keywords = self._initialize_keywords(keywords)
        self.api_url = "https://api.textcort¬ex.com/v1/texts/completions"

    def _initialize_keywords(self, keywords: List[str]) -> Dict[str, float]:
        """Convert keywords list to dictionary with weights"""
        keyword_weights = {
            # Technical Skills (higher weight)
            'Python': 1.5, 'Java': 1.5, 'JavaScript': 1.5, 'SQL': 1.5, 
            'AWS': 1.5, 'Docker': 1.5, 'Machine Learning': 1.5,

            # Soft Skills (medium weight)
            'Leadership': 1.2, 'Communication': 1.2, 'Problem Solving': 1.2,
            'Project Management': 1.2, 'Collaboration': 1.2,

            # Common Action Words (normal weight)
            'Developed': 1.0, 'Implemented': 1.0, 'Led': 1.0, 'Managed': 1.0
        }

        # Set default weight 1.0 for any keyword not in the predefined weights
        return {k: keyword_weights.get(k, 1.0) for k in keywords}

    def analyze(self):
        """Perform complete resume analysis"""
        # Find sections with their content
        sections_analysis = self._analyze_sections()
        section_score = self._calculate_section_score(sections_analysis)

        # Find and analyze keywords
        keywords_found = self._identify_keywords()
        keyword_score = self._calculate_keyword_score(keywords_found)

        # Check contact information
        contact_info = self._extract_contact_info()
        contact_score = self._calculate_contact_score(contact_info)

        # Calculate length and formatting score
        formatting_analysis = self._analyze_formatting()
        format_score = self._calculate_format_score(formatting_analysis)

        # Calculate total score with detailed breakdown
        total_score = round(section_score + keyword_score + contact_score + format_score)

        return {
            'total_score': total_score,
            'section_score': section_score,
            'keyword_score': keyword_score,
            'contact_score': contact_score,
            'format_score': format_score,
            'sections_found': sections_analysis['found_sections'],
            'section_details': sections_analysis['details'],
            'keywords_found': keywords_found,
            'contact_info': contact_info,
            'formatting_details': formatting_analysis,
            'estimated_pages': formatting_analysis['estimated_pages']
        }

    def _analyze_sections(self):
        """Analyze sections and their content quality"""
        found_sections = []
        section_details = {}

        for section in self.standard_sections:
            if re.search(rf'\b{section}\b', self.text, re.IGNORECASE):
                found_sections.append(section)

                # Find section content
                pattern = rf'{section}.*?(?={"|".join(self.standard_sections)}|$)'
                content_match = re.search(pattern, self.text, re.IGNORECASE | re.DOTALL)
                content = content_match.group(0) if content_match else ""

                # Analyze section content
                word_count = len(content.split())
                bullet_points = len(re.findall(r'[•\-\*]', content))

                section_details[section] = {
                    'word_count': word_count,
                    'bullet_points': bullet_points,
                    'has_numbers': bool(re.search(r'\d+', content)),
                    'quality_score': min(5, (word_count / 50) + (bullet_points / 3))
                }

        return {
            'found_sections': found_sections,
            'details': section_details
        }

    def _identify_keywords(self):
        """Identify keywords and their context in the resume"""
        found_keywords = []
        for keyword in self.keywords:
            if re.search(rf'\b{keyword}\b', self.text, re.IGNORECASE):
                found_keywords.append(keyword)
        return found_keywords

    def _extract_contact_info(self):
        """Extract and validate contact information"""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        phone_pattern = r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
        linkedin_pattern = r'linkedin\.com/\w+'

        email = re.search(email_pattern, self.text)
        phone = re.search(phone_pattern, self.text)
        linkedin = re.search(linkedin_pattern, self.text)

        return {
            'email': email.group() if email else None,
            'phone': phone.group() if phone else None,
            'linkedin': linkedin.group() if linkedin else None
        }

    def _analyze_formatting(self):
        """Analyze resume formatting and structure"""
        word_count = len(self.text.split())
        lines = self.text.split('\n')

        analysis = {
            'estimated_pages': word_count / 500,  # Updated estimate
            'avg_line_length': sum(len(line.split()) for line in lines) / len(lines),
            'bullet_point_ratio': len(re.findall(r'[•\-\*]', self.text)) / len(lines),
            'whitespace_ratio': self.text.count('\n') / len(self.text),
            'number_usage': len(re.findall(r'\d+', self.text)) / word_count
        }

        return analysis

    def _calculate_section_score(self, section_analysis):
        """Calculate section score based on presence and quality"""
        found_sections = section_analysis['found_sections']
        details = section_analysis['details']

        # Base score for number of sections
        if len(found_sections) >= 5:
            base_score = 20
        elif len(found_sections) >= 3:
            base_score = 15
        else:
            base_score = 10

        # Quality multiplier based on section content
        quality_scores = [details[section]['quality_score'] for section in found_sections]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0

        # Final section score
        return min(30, base_score + (avg_quality * 2))

    def _calculate_keyword_score(self, keywords_found):
        """Calculate keyword score based on presence and weights"""
        if not keywords_found:
            return 0

        total_weight = sum(self.keywords[k] for k in self.keywords)
        found_weight = sum(self.keywords[k] for k in keywords_found)

        return min(30, (30 * found_weight) / total_weight)

    def _calculate_contact_score(self, contact_info):
        """Calculate contact information score"""
        score = 0
        if contact_info['email']:
            score += 8
        if contact_info['phone']:
            score += 8
        if contact_info['linkedin']:
            score += 4
        return score

    def _calculate_format_score(self, formatting):
        """Calculate formatting and structure score"""
        score = 0

        # Length score
        if 1.0 <= formatting['estimated_pages'] <= 2.0:
            score += 8
        elif 0.8 <= formatting['estimated_pages'] <= 2.5:
            score += 5

        # Bullet point usage
        if 0.2 <= formatting['bullet_point_ratio'] <= 0.8:
            score += 4

        # Line length consistency
        if 8 <= formatting['avg_line_length'] <= 15:
            score += 4

        # Number usage (metrics/quantification)
        if 0.05 <= formatting['number_usage'] <= 0.15:
            score += 4

        return score

    def get_ai_recommendations(self):
        """Generate AI-powered recommendations using the free model API"""
        try:
            analysis_results = self.analyze()
            sections_missing = list(set(self.standard_sections) - set(analysis_results['sections_found']))
            keywords_missing = list(set(self.keywords) - set(analysis_results['keywords_found']))

            # Construct a prompt for the AI
            prompt = f"""Analyze this resume and provide specific recommendations for ATS optimization:

Resume Analysis:
- Current ATS Score: {analysis_results['total_score']}/100
- Sections present: {analysis_results['sections_found']}
- Missing sections: {sections_missing}
- Keywords found: {analysis_results['keywords_found']}
- Missing important keywords: {keywords_missing}
- Contact information: {"Complete" if all(analysis_results['contact_info'].values()) else "Incomplete"}
- Length: {analysis_results['estimated_pages']} pages

Please provide specific recommendations for improving this resume's ATS compatibility."""

            response = get_ai_response(prompt)

            if response["status_code"] == 200:
                print("API response received")
                return response["content"]
            else:
                print("No response from the API")
                return self._get_fallback_recommendations(analysis_results)

        except Exception as e:
            print(f"Error generating AI recommendations: {str(e)}")
            return self._get_fallback_recommendations(analysis_results)

    def _get_fallback_recommendations(self, analysis_results):
        """Generate basic recommendations based on analysis results"""
        recommendations = []

        if len(analysis_results['sections_found']) < 3:
            recommendations.append("❗ Add more standard sections to your resume:")
            for section in set(self.standard_sections) - set(analysis_results['sections_found']):
                recommendations.append(f"  - Consider adding a '{section}' section")

        if len(analysis_results['keywords_found']) < len(self.keywords) * 0.5:
            recommendations.append("\n❗ Incorporate more relevant keywords:")
            important_missing = list(set(self.keywords) - set(analysis_results['keywords_found']))[:5]
            for keyword in important_missing:
                recommendations.append(f"  - Add examples of your experience with '{keyword}'")

        if not all(analysis_results['contact_info'].values()):
            recommendations.append("\n❗ Contact Information:")
            if not analysis_results['contact_info']['email']:
                recommendations.append("  - Add a professional email address")
            if not analysis_results['contact_info']['phone']:
                recommendations.append("  - Include a phone number")

        if analysis_results['estimated_pages'] < 1:
            recommendations.append("\n❗ Resume Length:")
            recommendations.append("  - Expand your resume to at least one full page")
        elif analysis_results['estimated_pages'] > 2:
            recommendations.append("\n❗ Resume Length:")
            recommendations.append("  - Consider condensing your resume to 1-2 pages")

        if not recommendations:
            recommendations = [
                "✅ Your resume contains good content for ATS compatibility.",
                "Consider these general improvements:",
                "- Review and update your achievements with specific metrics",
                "- Ensure consistent formatting throughout",
                "- Use bullet points for better readability"
            ]

        return "\n".join(recommendations)