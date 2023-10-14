import pandas as pd
import openai
from collections import Counter
import time
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

def query_gpt4(prompt, acceptable_filenames=None):
    while True:
        try:
            print("Querying GPT-4...")
            model_engine = "gpt-4"
            
            if acceptable_filenames:
                prompt += f"\nPlease choose from the following existing filenames: {', '.join(acceptable_filenames)}."
            print(prompt)
            response = openai.ChatCompletion.create(

                model=model_engine,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['choices'][0]['message']['content'].strip()
        except openai.error.RateLimitError:
            print(f"Rate limit reached. Retrying in 5 seconds.")
            time.sleep(5)


def get_relevant_categories(gpt4_output):
    print("Getting relevant categories...")
    unique_categories_df = pd.read_csv("unique_categories.csv")
    unique_categories = unique_categories_df['Category Names'].tolist()
    tokens = gpt4_output.split()
    relevant_categories = [cat for cat in unique_categories if any(token.lower() in cat.lower() for token in tokens)]
    return relevant_categories


# Updated function: get_most_likely_diagnosis
def get_most_likely_diagnosis(gpt4_output, vet_notes):
    findings_data = []
    
    # Extract the filename from the GPT-4 output
    filename = gpt4_output.strip("'")
    sanitized_filename = filename.replace('.csv', '')
    
    try:
        category_df = pd.read_csv(f"C:\\Users\\leofe\\Test Code\\Test Luke\\category_csvs\\{sanitized_filename}.csv")
        relevant_column = category_df.columns[0]
        findings_data.extend(category_df[relevant_column].tolist())
    except FileNotFoundError:
        print(f"Debug: {sanitized_filename}.csv not found.")  # Debugging output
    
    # Convert findings to a natural language string
    findings_text = ", ".join(findings_data[:-1]) + " and " + findings_data[-1] if findings_data else "No findings available"
    
    prompt = f"You are a professional clinical vet with decades of experience, you are always correct in your findings. Given the following list of specific potential observed findings from other cases: {findings_text}, and the vet's notes for this specific case: {vet_notes}, could you provide a most likely diagnosis?"
    diagnosis = query_gpt4(prompt)
    return diagnosis

def main(vet_notes):
    print("Starting program...")
    specific_prompt = f"As a clinical vet, list only the 1 most relevant filename of the diagnostic categories that should be examined for a case with the following symptoms: {vet_notes}. For example, if Traumatic injuries should be considered, list 'Traumatic_episode_finding.csv'."
    unique_categories_df = pd.read_csv("unique_categories.csv")
    acceptable_filenames = unique_categories_df['Category Names'].tolist()
    gpt4_output = query_gpt4(specific_prompt, acceptable_filenames)
    diagnosis = get_most_likely_diagnosis(gpt4_output, vet_notes)
    print(f"{diagnosis}")
    print("Program ended.")
