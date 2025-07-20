# pip install vellum-ai
import os
import json
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
        dict: Structured learning content with overall_topic, subtopics, summaries, and quiz questions
    """
    try:
        result = client.execute_workflow(
            workflow_deployment_name="dual-wield",
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

        # Parse the JSON output from Vellum
        outputs = result.data.outputs
        
        print(f"🔍 Debug: Found {len(outputs)} outputs from Vellum")
        
                # Find the structured data in the outputs
        learning_content = None
        for i, output in enumerate(outputs):
            print(f"🔍 Output {i}: {type(output)}")
            if hasattr(output, 'value'):
                print(f"   Value type: {type(output.value)}")
                if isinstance(output.value, dict):
                    # The value is already a dictionary
                    if 'overall_topic' in output.value and 'subtopic' in output.value:
                        # Validate the new structure with Summaries as array
                        valid_structure = True
                        for subtopic in output.value.get('subtopic', []):
                            if 'Summaries' in subtopic:
                                summaries = subtopic['Summaries']
                                if not isinstance(summaries, list):
                                    print(f"   ❌ Summaries should be an array, got: {type(summaries)}")
                                    valid_structure = False
                                    break
                                for summary in summaries:
                                    if not isinstance(summary, dict) or 'Bullet_Point' not in summary or 'Read_Status' not in summary:
                                        print(f"   ❌ Summary should have Bullet_Point and Read_Status")
                                        valid_structure = False
                                        break
                        
                        if valid_structure:
                            learning_content = output.value
                            print(f"   ✅ Matches expected structure!")
                            break
                        else:
                            print(f"   ❌ Structure validation failed")
                    else:
                        print(f"   ❌ Dictionary doesn't match expected structure")
                        print(f"   Keys found: {list(output.value.keys())}")
                elif isinstance(output.value, str):
                    # Try to parse as JSON string
                    try:
                        json_data = json.loads(output.value)
                        if 'overall_topic' in json_data and 'subtopic' in json_data:
                            learning_content = json_data
                            print(f"   ✅ Valid JSON found and matches structure!")
                            break
                        else:
                            print(f"   ❌ JSON doesn't match expected structure")
                            print(f"   Keys found: {list(json_data.keys())}")
                    except json.JSONDecodeError as e:
                        print(f"   ❌ Not valid JSON: {e}")
                else:
                    print(f"   ❌ Unexpected value type: {type(output.value)}")
            else:
                print(f"   No 'value' attribute")
        
        if learning_content:
            return learning_content
        else:
            print("❌ No valid structured data found in Vellum outputs")
            print("📄 Raw outputs for debugging:")
            for i, output in enumerate(outputs):
                print(f"  Output {i}: {output}")
            return None
        
    except Exception as e:
        print(f"❌ Error running Vellum workflow: {e}")
        return None

# Example usage
if __name__ == "__main__":
    test_text = "This is a test of the Vellum workflow"
    learning_content = run_vellum_workflow(test_text)
    if learning_content:
        print("✅ Learning content structured successfully!")
        print(f"📚 Overall topic: {learning_content.get('overall_topic', 'N/A')}")
        print(f"📝 Number of subtopics: {len(learning_content.get('subtopic', []))}")
        for i, subtopic in enumerate(learning_content.get('subtopic', [])):
            print(f"  {i+1}. {subtopic.get('section_title', 'N/A')}")
            print(f"     Summary: {subtopic.get('Summaries', {}).get('Bullet_Point', 'N/A')[:50]}...")
            print(f"     Quiz questions: {len(subtopic.get('quiz_questions', []))}")
    else:
        print("❌ Failed to get structured learning content")
