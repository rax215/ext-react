import google.generativeai as genai
import os

# Define common text file extensions to attempt reading
TEXT_EXTENSIONS = {'.txt', '.py', '.js', '.html', '.css', '.json', '.md', '.csv', '.xml', '.yaml', '.yml'}

def generate_text_from_directory(prompt, directory_path, api_key):
    """Generates text using Gemini, incorporating content from all text files in a directory."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')

    contents = [prompt] # Start with the main prompt

    if not os.path.isdir(directory_path):
        return f"Error: Provided path is not a valid directory: {directory_path}"

    # Walk through the directory and subdirectories
    for root, _, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            _, extension = os.path.splitext(filename)

            # Check if the file has a common text extension
            if extension.lower() in TEXT_EXTENSIONS:
                try:
                    with open(file_path, "r", encoding="utf-8", errors='ignore') as text_file: # Ignore decoding errors
                        file_content = text_file.read()
                    # Add file content, indicating its path relative to the input directory
                    relative_path = os.path.relpath(file_path, directory_path)
                    contents.append(f"\n--- Content from {relative_path} ---\n{file_content}")
                except Exception as e:
                    print(f"Warning: Could not read file {file_path}: {e}") # Print warning but continue

    if len(contents) == 1: # Only the initial prompt was added
         return "No readable text files found in the specified directory."

    try:
        response = model.generate_content(contents)
        if hasattr(response, 'text'):
            return response.text
        else:
            print(f"DEBUG: Full response object: {response}")
            return "Response received, but no text content found."
    except Exception as e:
        # Provide more context on API errors if possible
        return f"Error generating content from Gemini API: {e}"

if __name__ == '__main__':
    # --- Configuration ---
    # Load securely in production!
    api_key = "AIzaSyAUhsbXRwKKmff5mDcy-GwZJuoAZ5-vvWE"
    # Define the prompt directly in the script
    with open('prompt.txt', 'r') as f:
            prompt_template = f.read()
    prompt = prompt_template
    # Define the directory path directly in the script
    directory_to_process = "ext" # Example: process the current directory where the script is run
    # --- End Configuration ---

    # Validate directory path
    if not os.path.isdir(directory_to_process):
        print(f"Error: The directory path '{directory_to_process}' does not exist or is not a directory.")
        exit(1)

    # Optional: Create a dummy file for testing if running in current dir and it's empty
    if directory_to_process == "./ext":
        dummy_file_path = "dummy_readme.md" # Example dummy file
        # Check if the directory is truly empty or only contains this script/requirements
        is_effectively_empty = True
        try:
            for item in os.listdir(directory_to_process):
                 if item not in ['gemini_api.py', 'requirements.txt', dummy_file_path, '.git', '__pycache__']: # Ignore common/script files
                     is_effectively_empty = False
                     break
        except FileNotFoundError:
             pass # Directory doesn't exist yet, handled above

        if is_effectively_empty and not os.path.exists(dummy_file_path):
             try:
                 with open(dummy_file_path, "w") as f:
                     f.write("# Dummy Project\nThis is a test file for the Gemini API script.")
                 print(f"Created dummy file for testing: {dummy_file_path}")
             except Exception as e:
                 print(f"Warning: Could not create dummy file {dummy_file_path}: {e}")


    result = generate_text_from_directory(prompt, directory_to_process, api_key)
    print("\n--- Gemini Response ---")
    print(result)
