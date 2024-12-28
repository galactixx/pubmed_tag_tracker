# PubMed Tag Tracker

A lightweight Python script that automatically scrapes and tracks PubMed tag metadata daily, providing insights into the latest tags being used in PubMed's database. Ideal for researchers, developers, or anyone interested in monitoring trends in PubMed metadata.

## Features

- Scrapes metadata for all actively used PubMed tags.
- Stores the data in JSON format for easy integration and analysis.
- Provides detailed information about each tag, including its abbreviation, name, and description.
- Includes a GitHub Action that automatically runs the scraper daily at midnight and updates the JSON file.

## Repository Structure

```
pubmed_tag_tracker/
├── .github/workflows/   # CI/CD workflows
├── .gitignore           # Git ignore file
├── LICENSE              # Project license
├── README.md            # Project documentation
├── pubmed_tags.json     # Scraped PubMed tag metadata
├── requirements.txt     # Python dependencies
├── scraper.py           # The main scraper script
```

## How It Works

The scraper, `scraper.py`, collects data from PubMed's database and stores it in `pubmed_tags.json`. This JSON file contains a comprehensive list of PubMed tags with detailed descriptions, making it a valuable resource for understanding and utilizing PubMed metadata.

A GitHub Action is set up in this repository to run `scraper.py` every day at midnight (UTC). The JSON file is updated automatically, ensuring the data is always current.

Here’s an example entry from `pubmed_tags.json`:

```json
{
    "Tag": "AU",
    "Name": "Author",
    "Description": "Authors"
}
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/pubmed_tag_tracker.git
   ```
2. Navigate to the project directory:
   ```bash
   cd pubmed_tag_tracker
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the scraper script manually:
   ```bash
   python scraper.py
   ```
   This will update the `pubmed_tags.json` file with the latest metadata.

2. Alternatively, rely on the GitHub Action to automatically update the JSON file daily.

3. Access the scraped data in `pubmed_tags.json` for analysis or integration into other projects.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

This project was inspired by the need to monitor trends and changes in PubMed's metadata, providing an up-to-date and accessible resource for researchers and developers.

---
