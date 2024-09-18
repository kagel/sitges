# Sitges Film Festival Movie Parser

This repository contains a Python script that reads JSON data from the Sitges Film Festival website, processes the data, applies customizable filters, and outputs a composite CSV file containing detailed information about film sessions. The script also scrapes additional director information from the festival's website.

The purpose of this project is to help you prepare efficiently for the Sitges Film Festival, especially when time is of the essence. With only a couple of days before tickets go on sale, you need to quickly study the festival program to make informed decisions on which films to prioritize. This script automates the process of organizing and filtering the extensive movie list, allowing you to focus on the hottest and most relevant films based on your preferences. It ensures you're well-prepared to act fast when tickets become available, giving you an edge in securing seats for the most sought-after movies.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Filters](#filters)
- [Output](#output)
- [Notes](#notes)
- [License](#license)

## Features

- Reads and processes multiple JSON files containing film, category, session, and location data.
- Merges data across different JSON sources to create a comprehensive CSV output.
- Scrapes director names and biographies from film detail pages using web scraping.
- Applies customizable filters to exclude unwanted films or sessions based on time, film type, and genre.
- Reports skipped sessions and films due to applied filters for transparency.

## Prerequisites

- Python 3.6 or higher
- Required Python packages:
    - `requests`
    - `beautifulsoup4`

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/kagel/sitges.git
   cd sitges
   ```

2. **Install the required packages:**

   You can install the required packages using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   **Note:** If you don't have a `requirements.txt` file, you can install the packages individually:

   ```bash
   pip install requests beautifulsoup4
   ```

3. **Place JSON files:**

   Ensure the following JSON files are placed in the same directory as the script:

    - `2024.json`
    - `categories.json`
    - `list.json`
    - `sessions.json`

   These files should contain the data as structured from the Sitges Film Festival website.

## Usage

Run the script using Python:

```bash
python sitges_parser.py
```

The script will process the data, apply filters, scrape additional information, and generate an output CSV file named `composite_sessions.csv`.

### Command-Line Arguments (Optional)

You can modify the script to accept command-line arguments for flexibility. For example, you can specify the paths to the JSON files or the output CSV file.

## Filters

The script includes filters defined in a declarative style at the top of the script. You can easily enable or disable filters and adjust their settings.

### Available Filters

1. **Time of Day Filter**

    - **Purpose:** Exclude sessions that start earlier than a specified time on certain days.
    - **Settings:**
        - `enabled`: `True` or `False` to enable or disable the filter.
        - `excluded_days`: List of days (e.g., `['Monday', 'Tuesday', 'Wednesday', 'Thursday']`) to apply the filter.
        - `earliest_allowed_time`: Time in `HH:MM` format (e.g., `'15:00'`).

2. **Category Filter**

    - **Purpose:** Exclude films of certain types or genres.
    - **Settings:**
        - `enabled`: `True` or `False` to enable or disable the filter.
        - `types_to_exclude`: List of film types to exclude (e.g., `['Short film', 'Clip', 'Series', 'Teaser', 'Extra']`).
        - `genres_to_exclude`: List of genres to exclude (e.g., `['Animation', 'Live action & Animation']`).

### Adjusting Filters

Open the script and locate the `filters` dictionary near the top:

```python
filters = {
    'time_filter': {
        'enabled': True,
        'excluded_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday'],
        'earliest_allowed_time': '15:00',
    },
    'category_filter': {
        'enabled': True,
        'types_to_exclude': ['Short film', 'Clip', 'Series', 'Teaser', 'Extra'],
        'genres_to_exclude': ['Animation', 'Live action & Animation'],
    },
}
```

Modify the `enabled` keys or adjust the lists to suit your preferences.

### Example

To disable the time filter, set `enabled` to `False`:

```python
filters['time_filter']['enabled'] = False
```

## Output

The script generates a CSV file named `composite_sessions.csv` containing the following columns:

- **Session Information:**
    - Session ID
    - Session Start Date
    - Session End Date
    - Session Duration
    - Session Location
    - Session Talent Presence
    - Session Q&A
    - Session Day
- **Film Information:**
    - Film ID
    - International Title
    - Original Title
    - Year
    - Duration
    - Directors
    - Director Biography
    - Synopsis (English)
    - Credits (English)
    - Genres
    - Sections
    - Categories
    - Awards
    - Types
    - Languages
    - Countries
    - Film URL

### Skipped Items Reporting

The script reports to the console when sessions or films are skipped due to the applied filters. This provides transparency and allows you to adjust filters if needed.

## Notes

- **Data Accuracy:** The script relies on the structure of the JSON files and the Sitges Film Festival website. Changes to the website or data format may require updates to the script.
- **Web Scraping Ethics:**
    - Ensure compliance with the website's [Terms of Service](https://sitgesfilmfestival.com/en/terms-service) and [Robots.txt](https://sitgesfilmfestival.com/robots.txt) policies.
    - Use the script responsibly and avoid overloading the website with excessive requests.
- **Performance Considerations:**
    - Scraping multiple film pages can be time-consuming. Consider implementing caching or limiting the number of requests if necessary.
    - The script includes basic error handling for network issues or unexpected data formats.

## License

This project is licensed under the [MIT License](LICENSE).

---

**Disclaimer:** This script is intended for educational and personal use. The author is not affiliated with the Sitges Film Festival. Always respect data privacy laws and website terms when accessing and using online content.
