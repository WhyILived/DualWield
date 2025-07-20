# pip install vellum-ai
import os
from pathlib import Path
from dotenv import load_dotenv
from vellum.client import Vellum
import vellum.types as types

# Load .env from root directory
project_root = Path(__file__).parent.parent
load_dotenv(project_root / '.env')

# create your API key here: https://app.vellum.ai/api-keys#keys
client = Vellum(
  api_key=os.environ["VELLUM_API_KEY"]
)

def run_vellum_workflow(text_content: str):
    """
    Run Vellum workflow with the given text content
    
    Args:
        text_content (str): The text to process through the workflow
    
    Returns:
        The workflow outputs
    """
    try:
        result = client.execute_workflow(
            workflow_deployment_name="teach-bot",
            release_tag="LATEST",
            inputs=[
                types.WorkflowRequestStringInputRequest(
                    name="text",
                    type="STRING",
                    value=text_content,
                ),
            ],
        )

        if result.data.state == "REJECTED":
            raise Exception(result.data.error.message)

        return result.data.outputs
        
    except Exception as e:
        print(f"Error running Vellum workflow: {e}")
        return None

# Example usage
if __name__ == "__main__":
    test_text = "This is a test of the Vellum workflow"
    outputs = run_vellum_workflow(test_text)
    print("Workflow outputs:", outputs)
