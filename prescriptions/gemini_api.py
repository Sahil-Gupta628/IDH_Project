import os
import google.generativeai as genai
import markdown
from django.conf import settings

# Import your API key
GEMINI_API_KEY = "AIzaSyB76_e0Roy5UPSLARsgHDRyMSFBOdmSjB4" #"Replace with your actual API key"

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-exp")

def process_prescription_image(image_path):
    """
    Process the prescription image with Gemini API
    """
    # Read image data
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # Prepare image for API
    picture = {
        "mime_type": "image/png",  # Adjust based on actual image type
        "data": image_data
    }
    
    # Extract prescription details
    prescription_prompt = """
    Analyze this prescription image and extract:
    1. All medicines prescribed
    2. Their dosages
    3. Frequency of intake
    4. Duration of treatment
    Provide the information in a structured format.
    Skip any introductory or concluding remarks.
    """
    prescription_response = model.generate_content([prescription_prompt, picture])
    extracted_text = markdown.markdown(prescription_response.text)
    
    # Get detailed medicine information
    medicine_prompt = """
    For each medicine mentioned in the prescription, provide:
    1. Brief description
    2. Common uses
    3. Potential side effects
    4. Important precautions
    5. A link to buy it online (format as [Buy here](https://www.google.com/search?q=buy+<medicine>))
    Format as structured markdown.
    """
    medicine_info = model.generate_content([medicine_prompt, prescription_response.text])
    medicine_info_html = markdown.markdown(medicine_info.text)
    
    return extracted_text, medicine_info_html