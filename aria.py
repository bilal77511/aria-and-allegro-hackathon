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

    def generate_poem(self, style="Allama Iqbal", verses=2, language="english"):
        """
        Generate a poem using ARIA
        
        Args:
            style (str): The style of poetry (default: "Allama Iqbal")
            verses (int): Number of verses to generate (default: 2)
            language (str): Language for the poem (default: "english")
            
        Returns:
            str: Generated poem
        """
        prompt = f"""
        Write a short, poem in {style} style in {language}.
        motivating poem only {verses} verses
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