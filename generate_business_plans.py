import os
import csv
import subprocess
from datetime import datetime
import multiprocessing
from tqdm import tqdm  # For progress bar

# Get the script's directory to ensure file paths are correctly set
script_directory = os.path.dirname(os.path.abspath(__file__))
output_directory = os.path.join(script_directory, "Generated_Business_Plans")

# Ensure the output directory exists, creating it if necessary
os.makedirs(output_directory, exist_ok=True)

# Path to the business details CSV file
business_csv = os.path.join(script_directory, "businesses.csv")

# Check for required dependencies
def check_dependencies():
    """Checks if required dependencies (tqdm and Ollama AI model) are installed."""
    missing = []
    try:
        import tqdm  # noqa: F401 (Ensuring tqdm is installed)
    except ImportError:
        missing.append("tqdm")

    # Verify if Ollama AI model is installed
    if subprocess.run(["which", "ollama"], capture_output=True, text=True).returncode != 0:
        missing.append("ollama")

    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        print("Please install them before running the script.")
        exit(1)

# Load business details from the CSV file
def load_businesses():
    """Loads business information from the CSV file and ensures proper formatting."""
    businesses = []
    try:
        with open(business_csv, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                if len(row) >= 4:  # Ensure there are enough columns to prevent errors
                    businesses.append({
                        'name': row[0].strip(),
                        'problem': row[1].strip(),
                        'solution': row[2].strip(),
                        'landing_page': row[3].strip()
                    })
    except FileNotFoundError:
        print(f"Error: {business_csv} not found. Please ensure the CSV file exists.")
        exit(1)
    return businesses

# Generate a sanitized filename based on business name
def generate_filename(name):
    """Creates a file-safe title using business name and timestamp to avoid conflicts."""
    title = name.replace(" ", "_").lower()
    title += "_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return title

# Generate a business plan using a local AI model via Ollama
def generate_business_plan(business, model="mistral"):
    """Generates a structured business plan using the AI model."""
    prompt = (f"Write a detailed business plan for a company called '{business['name']}'.\n"
              f"1. Executive Summary\n"
              f"2. Problem Statement: {business['problem']}\n"
              f"3. Solution: {business['solution']}\n"
              f"4. Business Model\n"
              f"5. Market Analysis\n"
              f"6. Marketing Strategy\n"
              f"7. Financial Plan\n"
              f"8. Conclusion\n"
              f"\nInclude a reference to the company's landing page: {business['landing_page']}.")
    
    try:
        # Call the AI model to generate text output
        response = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True
        )
        if response.returncode == 0:
            return response.stdout.strip()
        else:
            return "Error: AI model failed to generate business plan."
    except Exception as e:
        return f"Error: {e}"

# Save business plan to a text file
def save_business_plan(business, plan):
    """Saves the generated business plan into a uniquely named text file."""
    filename = generate_filename(business['name'])
    file_path = os.path.join(output_directory, f"{filename}.txt")
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(plan)
        return f"Business plan saved: {file_path}"
    except Exception as e:
        return f"Error saving file: {e}"

# Process a single business entry
def process_business(business):
    """Generates and saves a business plan for a single business entity."""
    try:
        plan = generate_business_plan(business)
        if "Error" in plan:
            raise Exception(plan)
        return save_business_plan(business, plan)
    except Exception as e:
        error_message = f"Error processing '{business['name']}': {e}\n"
        with open(os.path.join(output_directory, "error_log.txt"), "a", encoding="utf-8") as file:
            file.write(error_message)
        return error_message

# Main function to execute the script
def main():
    """Main execution function that processes all businesses in the CSV file."""
    check_dependencies()  # Ensure required dependencies are installed
    businesses = load_businesses()  # Load business data from CSV
    
    print(f"Processing {len(businesses)} businesses...\n")
    
    # Utilize multiprocessing to speed up business plan generation
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = list(tqdm(pool.imap(process_business, businesses), total=len(businesses), desc="Generating Business Plans"))
    
    # Summary Report
    success_count = sum(1 for r in results if "saved" in r)
    failure_count = len(businesses) - success_count

    print("\n=== Summary Report ===")
    print(f"Total Businesses: {len(businesses)}")
    print(f"Successful Plans: {success_count}")
    print(f"Failures: {failure_count}")
    
    if failure_count > 0:
        print("Check 'error_log.txt' for details.")
    
    print("\nBusiness plan generation complete!")

# Ensure the script runs only when executed directly
if __name__ == "__main__":
    main()

