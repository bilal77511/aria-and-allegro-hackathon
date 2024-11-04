from openai import OpenAI
from dotenv import load_dotenv
import os

class AriaTextGenerator:
    def __init__(self):
        """Initialize the ARIA text generator with API credentials"""
        load_dotenv()
        self.client = OpenAI(
            base_url=os.getenv('ARIA_BASE_URL'),
            api_key=os.getenv('ARIA_API_KEY')
        )

    def generate_poem(self, options, verses=1, language="english"):
        """
        Generate a poem using ARIA
        
        Args:
            options (dict): Contains details like title, tone, style, and keywords.
            verses (int): Number of verses to generate (default: 1)
            language (str): Language for the poem (default: "english")
            
        Returns:
            str: Generated poem
        """
        title = options.get('title', 'a beautiful theme')
        tone = options.get('tone', 'reflective')
        style = options.get('style')
        keywords = options.get('keywords')

        # Construct the initial prompt
        prompt = f"""
        Write a short, {verses}-verse poem about {title} in {language} language.
        The tone should be {tone}, with simple, evocative language.
        """

        # Conditionally add style and keywords if provided
        if style:
            prompt += f"\nThe style should reflect {style}."
        if keywords:
            prompt += f"\nUse the following keywords: {keywords}"

        
        try:
            response = self.client.chat.completions.create(
                model="aria",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ],
                stop=["<|im_end|>"],
                stream=False,
                temperature=0.6,
                max_tokens=1024,
                top_p=1
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise Exception(f"Failed to generate poem: {str(e)}")

    def generate_text(self, prompt):
        """
        Generate text using ARIA based on a custom prompt
        
        Args:
            prompt (str): The text prompt for generation
            
        Returns:
            str: Generated text
        """
        try:
            response = self.client.chat.completions.create(
                model="aria",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ],
                stop=["<|im_end|>"],
                stream=False,
                temperature=0.6,
                max_tokens=1024,
                top_p=1
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise Exception(f"Failed to generate text: {str(e)}")