import os
import sys
import time
import requests
import textwrap
from datetime import datetime

def main():
    api_key = os.environ.get("NASA_API_KEY")
    if not api_key:
        api_key = "DEMO_KEY"

    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&thumbs=true"
    
    max_retries = 3
    data = None
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            break  # Success
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"API attempt {attempt + 1} failed ({e}). Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print(f"Error fetching data from NASA API after {max_retries} attempts: {e}")
                sys.exit(1)
        
    date_str = data.get("date", datetime.utcnow().strftime("%Y-%m-%d"))
    title = data.get("title", "No Title")
    explanation = data.get("explanation", "")
    media_type = data.get("media_type", "image")
    copyright_info = data.get("copyright", "Public Domain").replace("\n", " ").strip()
    
    if media_type == "video":
        image_url = data.get("thumbnail_url", "")
    else:
        image_url = data.get("url", "")
        
    print(f"Successfully fetched APOD: {title} ({date_str})")

    # Write title to .today_title temp file
    with open(".today_title", "w", encoding="utf-8") as f:
        f.write(title)
        
    # Write to GITHUB_ENV if available for use in the next steps
    if "GITHUB_ENV" in os.environ:
        with open(os.environ["GITHUB_ENV"], "a", encoding="utf-8") as f:
            safe_title = title.replace("\n", " ")
            f.write(f"APOD_TITLE={safe_title}\n")
            f.write(f"APOD_DATE={date_str}\n")
            f.write(f"APOD_MEDIA_TYPE={media_type}\n")

    # Word wrap explanation
    wrapped_explanation = textwrap.fill(explanation, width=100)
    quoted_explanation = "\n".join(f"> {line}" for line in wrapped_explanation.split("\n"))
    
    image_md = f"![{title}]({image_url})" if image_url else ""
    
    new_entry = f"""## {date_str} — {title}
**Copyright:** {copyright_info}

{image_md}

{quoted_explanation}

---
"""

    # Ensure log directory exists
    log_dir = "log"
    os.makedirs(log_dir, exist_ok=True)

    dt = datetime.strptime(date_str, "%Y-%m-%d")
    year_month = dt.strftime("%Y-%m")
    log_file = os.path.join(log_dir, f"{year_month}.md")
    
    heading = f"# Cosmos Log — Month {year_month}\n\n"
    
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            existing_content = f.read()
    else:
        existing_content = ""
        
    # Prepend the new entry newest-first
    if existing_content.startswith(heading):
        body = existing_content[len(heading):].lstrip()
        final_log = heading + new_entry + "\n" + body
    else:
        final_log = heading + new_entry + "\n" + existing_content
        
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(final_log)
        
    # Update README.md
    readme_path = "README.md"
    short_exp = explanation[:280] + "..." if len(explanation) > 280 else explanation
    
    readme_block = f"""<!-- COSMOS-START -->
## 🔭 Today's Sky — {date_str}
### {title}

{image_md}

*{short_exp}*

📂 [Full archive in /log](./log/)
<!-- COSMOS-END -->"""

    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
            
        start_marker = "<!-- COSMOS-START -->"
        end_marker = "<!-- COSMOS-END -->"
        
        if start_marker in readme_content and end_marker in readme_content:
            start_idx = readme_content.find(start_marker)
            end_idx = readme_content.find(end_marker) + len(end_marker)
            new_readme = readme_content[:start_idx] + readme_block + readme_content[end_idx:]
        else:
            new_readme = readme_content.rstrip() + "\n\n" + readme_block + "\n"
    else:
        new_readme = readme_block + "\n"
        
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_readme)

if __name__ == "__main__":
    main()
