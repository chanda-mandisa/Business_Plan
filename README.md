# Business Plan Generator

This project automates the generation of business plans using a structured format and an AI model. It is designed to assist entrepreneurs in creating detailed business plans efficiently.

## Features

- Generates business plans based on predefined categories (e.g., problem, solution, market analysis).
- Uses a local AI model to draft business plans automatically.
- Saves business plans as text files with timestamped filenames.
- Supports batch processing using multiprocessing for efficiency.
- Logs errors to an error log file for debugging.

## Getting Started

This project enables users to generate structured business plans using a local AI model.

### Installation
#### Clone the Repository

```sh
git clone https://github.com/chanda-mandisa/Business_Plan.git
cd Business_Plan
```

### System Requirements

- Python 3.x
- Ollama AI model installed locally
- tqdm Python package (for progress visualization)

### Running the Script
#### Generate Business Plans:

```sh
python generate_business_plans.py
```

- The script will read from `businesses.csv` and generate business plans for each entry.
- Business plans will be saved in the `Generated_Business_Plans` directory.

## Usage

### Viewing Generated Business Plans

- Open the `Generated_Business_Plans` folder to access generated plans.
- Each plan is saved as a text file with a timestamped filename.

### Organizing Plans

- Move older plans into an archive folder to keep your workspace clean.

### Customization

#### Modify Business Inputs

- Edit `businesses.csv` and add new business ideas.
- Ensure each row contains: `name, problem, solution, landing_page`.

#### Adjust AI Model

- Modify `generate_business_plan()` in `generate_business_plans.py` to change AI prompts.
- Update the AI model name if using a different one.

## Troubleshooting

### Errors While Running `business_plan_generator.py`

- Ensure Ollama AI is installed and accessible.
- If `businesses.csv` is missing, create one following the sample format.
- Install missing dependencies using:

```sh
pip install tqdm
```

### Business Plans Not Generating Properly

- Check error logs in `Generated_Business_Plans/error_log.txt`.
- Ensure your CSV file is properly formatted.

## License

This project is licensed under the MIT License. See LICENSE for details.

## Contributions

Contributions are welcome! Feel free to submit a pull request or report issues.

## Author

Developed by [chanda-mandisa].


