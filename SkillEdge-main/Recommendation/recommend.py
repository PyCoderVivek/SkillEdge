import google.generativeai as genai
from django.conf import settings
from Performance.models import Subject
from django.db.models import Avg
import re
import urllib.parse

# Configure Gemini API using the key from settings.py
genai.configure(api_key=settings.GEMINI_API_KEY)


def get_gemini_suggestions_with_links(subject_name, marks, max_marks):
    """
    Get AI study suggestions with clean, working resource links.
    """
    try:
        # Define the Gemini model
        model = genai.GenerativeModel("gemini-2.0-flash")

        # Enhanced prompt for clearer, more specific recommendations
        prompt = (
            f"I have {subject_name} and scored {marks}/{max_marks}. "
            "Tell me if I'm weak or strong in this subject. "
            "Give a short, practical study tip (3 Lines) and include EXACTLY 2 high-quality resource links "
            "(1 video, 1 article or interactive tutorial). "
            "Make sure the links are specific to my needs and clearly different from each other."
        )

        # Get response from Gemini
        response = model.generate_content(prompt)

        # Clean Markdown-style formatting from the suggestion
        suggestion = re.sub(r"\*{1,2}(.+?)\*{1,2}", r"\1", response.text).strip()

        # Extract just the URLs from Markdown format
        markdown_links = re.findall(r"\[(.*?)\]\((https?://[^\s]+)\)", suggestion)
        clean_links = [link[1] for link in markdown_links]

        # Extract any extra plain URLs (not in markdown format)
        extra_links = re.findall(r"https?://[^\s,]+", suggestion)
        
        # Combine and clean all links
        all_links = clean_links + [link for link in extra_links if link not in clean_links]
        
        # Normalize links to prevent duplicates with different URL parameters
        normalized_links = []
        seen_domains = set()
        
        for link in all_links:
            # Parse the URL and get base domain
            parsed_url = urllib.parse.urlparse(link)
            base_domain = parsed_url.netloc
            
            # Skip if we've already seen this domain
            if base_domain in seen_domains:
                continue
                
            seen_domains.add(base_domain)
            normalized_links.append(link)
        
        # Limit to maximum 2 links
        final_links = normalized_links[:2]

        # Clean suggestion by removing Markdown links
        clean_suggestion = re.sub(r"\[.*?\]\((https?://[^\s]+)\)", "", suggestion).strip()
        # Remove any remaining URLs from the suggestion text
        for link in all_links:
            clean_suggestion = clean_suggestion.replace(link, "")
        
        # Clean up extra spaces and punctuation
        clean_suggestion = re.sub(r'\s+', ' ', clean_suggestion).strip()
        clean_suggestion = re.sub(r'\.{2,}', '.', clean_suggestion)
        clean_suggestion = re.sub(r'\s+([.,])', r'\1', clean_suggestion)

        return clean_suggestion, final_links

    except Exception as e:
        return f"AI suggestion failed: {e}", []


def get_recommendations(user):
    """
    Fetch user subjects and generate AI-powered recommendations with external resources.
    """
    # Get user's subjects
    subjects = Subject.objects.filter(semester__user=user)

    # Calculate user's average marks
    avg_marks = subjects.aggregate(Avg('obtained_marks'))['obtained_marks__avg']

    recommendations = []

    # Generate AI suggestions for subjects below average
    for subject in subjects:
        if subject.obtained_marks < avg_marks:
            ai_suggestion, ai_links = get_gemini_suggestions_with_links(
                subject.name, subject.obtained_marks, subject.max_marks
            )

            recommendations.append({
                'subject_name': subject.name,
                'marks': subject.obtained_marks,
                'max_marks': subject.max_marks,
                'suggestion': ai_suggestion,
                'links': ai_links
            })

    return recommendations
