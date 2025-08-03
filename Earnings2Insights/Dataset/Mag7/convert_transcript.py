import requests
import json
import sys
from datetime import datetime
import os

def fetch_transcript(symbol, quarter, api_key):
    url = f"https://www.alphavantage.co/query?function=EARNINGS_CALL_TRANSCRIPT&symbol={symbol}&quarter={quarter}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    
    # Check for API errors or empty response
    if 'Error Message' in data:
        raise Exception(f"API Error: {data['Error Message']}")
    if not data.get('transcript'):
        raise Exception("No transcript data available for the specified symbol and quarter.")
    
    return data

def convert_to_markdown(transcript_data):
    markdown = "## Financial Earnings Call\n\n"
    markdown += "### Prepared remarks\n"
    
    for entry in transcript_data.get('transcript', []):
        speaker = entry.get('speaker', '')
        title = entry.get('title', '')
        content = entry.get('content', '')
        
        # Check if this is the start of Q&A section
        if title.lower() == 'operator' and 'question' in content.lower():
            markdown += "\n### Q&A\n"
        
        # Format the speaker and content
        markdown += f"**{title}**\n"
        markdown += f": {content}\n\n"
    
    return markdown

def main():
    print("Note: Alpha Vantage API provides earnings call transcripts with a delay.")
    print("The most recent quarter's transcript may not be available immediately.\n")
    
    # Get inputs from user
    symbol = input("Enter ticker symbol (e.g., AAPL): ").strip().upper()
    quarter = input("Enter quarter (e.g., 2024Q4): ").strip().upper()
    api_key = os.environ.get('ALPHAVANTAGE_API_KEY')
    try:
        # Fetch transcript
        transcript_data = fetch_transcript(symbol, quarter, api_key)
        
        # Convert to markdown
        markdown_content = convert_to_markdown(transcript_data)
        
        # Generate output filenames
        json_file = f"Earnings2Insights/Dataset/Mag7/{symbol}_{quarter}.json"
        markdown_file = f"Earnings2Insights/Dataset/Mag7/{symbol}_{quarter}.md"
        
        # Save JSON response
        with open(json_file, 'w') as f:
            json.dump(transcript_data, f, indent=4)
        
        # Save markdown
        with open(markdown_file, 'w') as f:
            f.write(markdown_content)
            
        print(f"\nTranscript successfully converted and saved to {markdown_file}")
        print(f"JSON response saved to {json_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()