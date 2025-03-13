import os
import json
import logging
import google.generativeai as genai
from django.conf import settings

# Set up logging
logger = logging.getLogger(__name__)

# Initialize the Gemini API with your API key
genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_career_roadmap(interests, career_goals):
    """
    Generate a career roadmap using Gemini AI based on user interests and career goals
    """
    # Log the input data (without sensitive information)
    logger.info(f"Generating roadmap with interest length: {len(interests)} and career goals length: {len(career_goals)}")
    
    prompt = f"""
    I need a detailed career roadmap based on the following information:
    
    INTERESTS: {interests}
    CAREER GOALS: {career_goals}
    
    Please provide a comprehensive roadmap with the following structure:
    1. A title for the roadmap
    2. A brief description/overview of the career path
    3. A list of 5-7 milestones, each containing:
       - Milestone title
       - Description of what should be accomplished
       - Suggested timeframe
       - 2-3 resource recommendations (courses, books, tools) for each milestone
    
    Format the response as a valid JSON object with the following structure:
    {{
        "title": "Roadmap title",
        "description": "Overview of the roadmap",
        "milestones": [
            {{
                "title": "Milestone 1",
                "description": "Description of milestone 1",
                "time_frame": "Timeframe (e.g., '3-6 months')",
                "resources": [
                    {{
                        "title": "Resource 1 title",
                        "url": "URL if applicable",
                        "description": "Brief description of the resource",
                        "resource_type": "Course/Book/Tool/etc."
                    }}
                ]
            }}
        ]
    }}
    
    It's critical that your response is a valid JSON object following the exact structure above.
    """
    
    try:
        # Generate content using Gemini
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        
        # Log response received (but not the full content)
        logger.info(f"Received response from Gemini API of length: {len(response.text)}")
        
        # Try to extract JSON from the response, handling various response formats
        try:
            # First attempt: try to parse the entire response as JSON
            roadmap_data = json.loads(response.text)
            return roadmap_data
        except json.JSONDecodeError:
            # Second attempt: try to find JSON content within the response
            # Look for content between curly braces
            try:
                json_start = response.text.find('{')
                json_end = response.text.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    json_str = response.text[json_start:json_end]
                    roadmap_data = json.loads(json_str)
                    return roadmap_data
            except (json.JSONDecodeError, IndexError):
                # Log the error and response for debugging
                logger.error(f"Failed to parse JSON from response: {response.text[:200]}...")
                
                # Fall back to a default structure with an error message
                return {
                    "title": "Career Development Roadmap",
                    "description": f"""
                    We couldn't generate a specific roadmap from your current profile information.
                    
                    Please try updating your profile with more detailed information about:
                    - Your specific skills and technical background
                    - Areas of interest within your field
                    - Concrete career aspirations (roles, industries, etc.)
                    - Any timeframe you have in mind for your goals
                    
                    The more specific details you provide, the better the AI can generate a relevant roadmap.
                    """,
                    "milestones": [
                        {
                            "title": "Update Your Profile Information",
                            "description": "Enhance your profile with detailed interests and career goals to get a personalized roadmap.",
                            "time_frame": "As soon as possible",
                            "resources": [
                                {
                                    "title": "Edit Your Profile",
                                    "url": "/auth/profile/edit/",
                                    "description": "Add detailed information about your interests and career goals.",
                                    "resource_type": "Action"
                                }
                            ]
                        }
                    ]
                }
    except Exception as e:
        # Log any other exceptions that might occur
        logger.error(f"Error generating roadmap: {str(e)}")
        return {
            "title": "Career Development Roadmap",
            "description": "We encountered a technical issue while generating your roadmap. Please try again later.",
            "milestones": []
        } 