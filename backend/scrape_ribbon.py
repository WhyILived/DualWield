from seleniumbase import Driver
import json
import re
import time

def scrape_ribbon_scorecard(flow_id, interview_id):
    """
    Scrapes the Ribbon AI interview scorecard for a given flow and interview.
    
    Args:
        flow_id (str): The flow ID from the URL
        interview_id (str): The interview ID from the URL
    
    Returns:
        list: A list of dictionaries containing category, text, and score data
    """
    
    # Construct the URL
    url = f'https://app.ribbon.ai/recruit/interviews/{flow_id}/{interview_id}?tab=Scorecard'
    
    # Initialize the driver
    driver = Driver(browser="chrome", headless=True)  # Set headless=False to see the browser
    
    try:
        # Navigate to the scorecard page
        driver.get(url)
        
        # Wait for the page to load
        driver.wait_for_element_present('[aria-label="Expand"]', timeout=10)
        
        # Find all expand buttons
        expand_buttons = driver.find_elements('css selector', '[aria-label="Expand"]')
        print(f"Found {len(expand_buttons)} expand buttons")
        
        # Click only the first two buttons
        for i in range(min(2, len(expand_buttons))):
            try:
                driver.execute_script("arguments[0].click();", expand_buttons[i])
                time.sleep(1)  # Give time for content to load
                print(f"Clicked button {i+1}")
            except Exception as e:
                print(f"Error clicking button {i+1}: {e}")
        
        # Wait for content to fully load
        time.sleep(2)
        
        # Extract all the data
        data = []
        
        # Category names
        categories = ["Interview Score", "English Proficiency"]
        
        # Find all text elements - specifically spans with class="css-zw4nq7"
        text_elements = driver.find_elements('css selector', 'span.css-zw4nq7')
        print(f"Found {len(text_elements)} text elements")
        
        # Find all score elements - specifically spans with class="css-oqopj8"
        score_elements = driver.find_elements('css selector', 'span.css-oqopj8')
        print(f"Found {len(score_elements)} score elements")
        
        # Extract text from each element
        texts = []
        for element in text_elements:
            try:
                text = element.text.strip()
                if text:  # Only add non-empty texts
                    texts.append(text)
            except Exception as e:
                print(f"Error extracting text: {e}")
        
        # Extract only actual scores (matching "X / 5" pattern)
        scores = []
        score_pattern = re.compile(r'^\d+\s*/\s*5$')
        
        for element in score_elements:
            try:
                text = element.text.strip()
                if text and score_pattern.match(text):  # Only add if it matches "X / 5" pattern
                    scores.append(text)
            except Exception as e:
                print(f"Error extracting score: {e}")
        
        print(f"Extracted {len(texts)} texts and {len(scores)} actual scores")
        
        # Pair texts with scores
        min_length = min(len(texts), len(scores))
        
        for i in range(min_length):
            text = texts[i]
            score = scores[i]
            
            # Determine which category this belongs to
            # First 4 items are Interview Score, next 4 are English Proficiency
            category = categories[0] if i < 4 else categories[1]
            
            data.append({
                'category': category,
                'text': text,
                'score': score
            })
        
        print(f"\nTotal items extracted: {len(data)}")
        print(f"Expected: 8 items (2 buttons × 4 items each)")
        
        return data
        
    except Exception as e:
        print(f"Error during scraping: {e}")
        return []
        
    finally:
        driver.quit()


# Example usage:
if __name__ == "__main__":
    # Example IDs from the original URL
    flow_id = "f77cc73e"
    interview_id = "59dbcbc7-704e-471a-b070-30accbff78b3"
    
    # Scrape the data
    result = scrape_ribbon_scorecard(flow_id, interview_id)
    
    # Print the result as JSON
    json_output = json.dumps(result, indent=4)
    print("\nExtracted Data:")
    print(json_output)
    
    # Save to file
    with open('scorecard_data.json', 'w') as f:
        f.write(json_output)
    print("\nData saved to scorecard_data.json")