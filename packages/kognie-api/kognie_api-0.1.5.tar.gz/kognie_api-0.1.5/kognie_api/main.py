import requests

class Kognie:
    """
    Kognie API client for generating text and images.
    """

    def __init__(self, api_key=None):
        """
        Initialize the Kognie API client.
        Args:
            api_key (str): Your API key for authentication.
        """
        self.api_key = api_key
        self.TEXT_ENDPOINT = "http://api2.kognie.com/text"
        self.IMAGE_ENDPOINT = "http://api2.kognie.com/image"

    def generateText(self,question, model="gpt-4"):
        """
        Function to send a text request to the Kognie API.
        Args:
            question (str): The question to ask the model.
            model (str): The model to use. Default is "gpt-4".
        Returns:
            dict: The response from the API.
        """
        url = self.TEXT_ENDPOINT
        params = {
            "question": question,
            "model": model
        }
        headers = {
            "x-key": self.api_key
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error: {response.status_code}, {response.text}"}

    def generateImage(self,question, model="dall-e-2", response_format="base64", aspect_ratio="1:1"):
        """
        Function to send an image request to the Kognie API.
        Args:
            question (str): The question to ask the model.
            model (str): The model to use. Default is "dall-e".
            response_format (str): The format of the response. Default is "base64".
            aspect_ratio (str): The aspect ratio of the image. Default is "1:1".
        Returns:
            dict: The response from the API.
        """
        url = self.IMAGE_ENDPOINT
        params = {
            "question": question,
            "model": model,
            "response_format": response_format,
            "aspect_ratio": aspect_ratio
        }
        headers = {
            "x-key": self.api_key
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error: {response.status_code}, {response.text}"}
