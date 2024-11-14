import os
import torch
from logly import logly
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("MODEL_NAME")
genai.configure(api_key=gemini_api_key)

# Configuration for 4-bit quantization
quantization_config = BitsAndBytesConfig(load_in_4bit=True)


def pipeline_tunnel(model, device):
    """
    Initialize a text generation pipeline with the specified model and device.

    Args:
        model (str): The name of the model to load for text generation.
        device (str): The device to load the model on ('cpu' or 'cuda').

    Returns:
        transformers.Pipeline: A text generation pipeline configured for the specified model and device.
    """
    logly.info(f"Using device: {device}")
    logly.info(f"Loading model: {model}")
    return pipeline(
        "text-generation",
        model=model,
        model_kwargs={
            "torch_dtype": torch.float16,
        },
        device=device,
    )


class Generate:
    """
    A class to generate emergency, disaster, and wartime reports based on given data.

    Attributes:
        report_data (list of dict): The data for the report, with each entry containing a title and summary.
        api (bool): A flag indicating whether to use the generative AI API (True) or local model (False).
    """

    def __init__(self, report_data, api=False):
        """
        Initialize the Generate class with report data and specify whether to use the API.

        Args:
            report_data (list of dict): The data for the report.
            api (bool): Set to True to use the generative AI API, False to use a local model (default is False).
        """
        self.report_data = report_data
        self.api = api

    def generate_report(self):
        """
        Generate a structured emergency report based on the input data. The report will include
        headlines, key highlights, and precautionary advice for emergency alerts.

        If `self.api` is True, it uses the generative AI API. Otherwise, it uses a local model.

        Returns:
            str: A formatted report in Markdown or an error message if generation fails.
        """
        # Format report data as a structured list for input
        formatted_data = "\n".join([f"- **{item['title']}**: {item['summary']}" for item in self.report_data])

        # Define the structured prompt to guide model output
        prompt_template = (
            "You are an expert emergency reporter tasked with creating a concise report on critical events like disasters, emergencies, pandemics, and wars. "
            "Use the following emergency alerts to generate a clear and actionable report. The report should include:\n\n"
            "1. **Title**: A clear and meaningful title for the emergency.\n"
            "2. **Explanation**: A brief but detailed explanation of the emergency.\n"
            "3. **Precautions**: Actionable precautions for people to stay safe.\n\n"
            "### Emergency Alerts:\n"
            f"{formatted_data}\n\n"
            "Generate a professional report based on the data. Ensure the content is directly related to emergencies and public safety."
        )

        if self.api:
            try:
                # Generate report text using the generative AI API
                report_text = genai.GenerativeModel(model_name='gemini-1.5-flash')
                response = report_text.generate_content(prompt_template)

                # Ensure the response is valid
                if response and hasattr(response, 'text') and response.text.strip():
                    logly.info(f"Generated report: {response.text}")
                    return f"### Emergency Report\n\n{response.text}"
                else:
                    logly.error("Generated report is empty or invalid.")
                    return "Error: Generated report is empty or invalid."

            except Exception as e:
                logly.error(f"Error generating report with API: {e}")
                return f"Error generating report with API: {e}"

        else:
            try:
                # Set device and quantization for local model
                device = "cuda" if torch.cuda.is_available() else "cpu"
                quantization = "4-bit"
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True) if quantization == "4-bit" else BitsAndBytesConfig(load_in_8bit=True)

                # Load tokenizer and text generation pipeline
                tokenizer = AutoTokenizer.from_pretrained(model_name, quantization_config=quantization_config)
                pipeline_model = pipeline_tunnel(model_name, device)

                # Generate report using local model pipeline
                logly.info(f"Prompt: {prompt_template}")
                outputs = pipeline_model(
                    prompt_template,
                    max_new_tokens=1250,
                    do_sample=True,
                    temperature=0.7,
                    top_k=50,
                    top_p=0.95
                )

                # Log the full generated text
                generated_text = outputs[0]["generated_text"][len(prompt_template):]

                # Check if the generated text is empty
                if generated_text.strip():
                    logly.info(f"Generated report: {generated_text}")
                    return generated_text
                else:
                    logly.error("Generated report is empty or invalid.")
                    return "Error: Generated report is empty or invalid."

            except Exception as e:
                logly.error(f"Error in pipeline: {e}")
                return f"Error in pipeline: {e}"

