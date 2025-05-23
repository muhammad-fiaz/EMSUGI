import os
import torch
from flask import session
from transformers import AutoTokenizer, BitsAndBytesConfig, pipeline
from logly import logly
from langchain_core.prompts import PromptTemplate
import google.generativeai as genai
from dotenv import load_dotenv
from modules.utils.check_for_cancel import check_for_cancel

# Load environment variables from .env file
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_model_name = os.getenv("GEMINI_MODEL_NAME")
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
        model_kwargs={"torch_dtype": torch.float16},  # Model precision
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

        # Define the structured prompt to guide model output using LangChain PromptTemplate
        prompt_template = PromptTemplate.from_template(
            "You are an expert emergency reporter. Using the following emergency alerts, create a brief report including:\n\n"
            "1. **Title**: A meaningful title for the emergency.\n"
            "2. **Explanation**: A brief summary of the emergency.\n"
            "3. **Precautions**: Clear, actionable steps to stay safe.\n\n"
            "### Emergency Alerts:\n"
            "{context}\n\n"
            "Generate a concise report based on the data, focusing on safety and emergency response."
        )

        # Truncate context if too long
        context_limit = 512  # Adjust based on model constraints
        truncated_context = formatted_data[:context_limit]

        # Format the prompt using LangChain PromptTemplate
        formatted_prompt = prompt_template.format(context=truncated_context)

        if self.api:
            try:
                # Generate report text using the Gemini API
                report_text = genai.GenerativeModel(model_name=gemini_model_name)
                response = report_text.generate_content(formatted_prompt)

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
                tokenizer = AutoTokenizer.from_pretrained(model_name, quantization_config=quantization_config)
                pipeline_model = pipeline_tunnel(model_name, device)

                # Generate report using local model pipeline
                logly.info(f"Prompt: {formatted_prompt}")
                outputs = pipeline_model(
                    formatted_prompt,
                    max_new_tokens=512,
                    do_sample=True,
                    temperature=0.7,
                    top_k=50,
                    top_p=0.95
                )

                # Extract the generated text
                generated_text = outputs[0]["generated_text"][len(formatted_prompt):].strip()

                # Check if the generated text is empty
                if generated_text:
                    logly.info(f"Generated report: {generated_text}")
                    return f"### Emergency Report\n\n{generated_text}"
                else:
                    logly.error("Generated report is empty or invalid.")
                    return "Error: Generated report is empty or invalid."

            except Exception as e:
                logly.error(f"Error in pipeline: {e}")
                return f"Error in pipeline: {e}"

