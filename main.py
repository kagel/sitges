import csv
import json

import requests
from bs4 import BeautifulSoup

# Read the JSON files
with open('2024.json', 'r', encoding='utf-8') as f:
    films_data = json.load(f)['films']  # assuming top-level key is 'films'

with open('categories.json', 'r', encoding='utf-8') as f:
    categories_data = json.load(f)

with open('list.json', 'r', encoding='utf-8') as f:
    list_data = json.load(f)

with open('sessions.json', 'r', encoding='utf-8') as f:
    sessions_data = json.load(f)

# Create mapping dictionaries
# Films mapping: film ID to film data
film_dict = {}
for film in films_data:
    film_dict[film['id']] = film


# Categories mapping
def create_mapping(data_list):
    mapping = {}
    for item in data_list:
        mapping[item['id']] = item['name']
    return mapping


genres = create_mapping(categories_data.get('genres', []))
sections = create_mapping(categories_data.get('sections', []))
categories = create_mapping(categories_data.get('categories', []))
awards = create_mapping(categories_data.get('awards', []))
types = create_mapping(categories_data.get('types', []))
languages = create_mapping(categories_data.get('languages', []))
countries = create_mapping(categories_data.get('countries', []))

# Locations mapping
locations = create_mapping(list_data.get('locations', []))

# Days mapping
days = {}
for day in sessions_data.get('days', []):
    days[day['id']] = day['name']

# Prepare CSV header
header = [
    'Session ID',
    'Session Start Date',
    'Session End Date',
    'Session Duration',
    'Session Location',
    'Session Talent',
    'Session QA',
    'Session Day',
    'Film ID',
    'Film International Title',
    'Film Original Title',
    'Film Year',
    'Film Duration',
    'Film Directors',
    'Director Biography',
    'Film Synopsis (en)',
    'Film Credits (en)',
    'Film Genres',
    'Film Sections',
    'Film Categories',
    'Film Awards',
    'Film Types',
    'Film Languages',
    'Film Countries',
    'Film URL'
]

# Process sessions and films
rows = []
progress = 0

for session in sessions_data.get('sessions', []):
    progress += 1
    print(f'Processing session {progress}/{len(sessions_data["sessions"])}')

    session_id = session.get('id', '')
    session_start = session.get('start_date', '')
    session_end = session.get('end_date', '')
    session_duration = session.get('duration', '')
    session_talent = session.get('talent', '')
    session_qa = session.get('qa', '')
    session_day_ids = session.get('days', [])
    session_day_names = [days.get(day_id, {}).get('en', '') for day_id in session_day_ids if day_id in days]
    session_locations = session.get('locations', [])
    session_location_names = [locations.get(loc_id, {}).get('en', '') for loc_id in session_locations if
                              loc_id in locations]

    # Use the first day and location if multiple are present
    session_day = session_day_names[0] if session_day_names else ''
    session_location = session_location_names[0] if session_location_names else ''

    session_films = session.get('films', [])
    for film_id in session_films:
        film = film_dict.get(film_id)
        if not film:
            continue  # Skip if film data not found

        film_international_title = film.get('international_title', '')
        film_original_title = film.get('original_title', '')
        film_year = film.get('year', '')
        film_duration = film.get('duration', '')
        film_synopsis = film.get('synopsis', {}).get('en', '')
        film_credits = film.get('credits', {}).get('en', '')


        # Map IDs to names
        def get_names(id_list, mapping):
            names = [mapping.get(id_, {}).get('en', '') for id_ in id_list if id_ in mapping]
            return '; '.join(names)


        film_genres_str = get_names(film.get('genres', []), genres)
        film_sections_str = get_names(film.get('sections', []), sections)
        film_categories_str = get_names(film.get('categories', []), categories)
        film_awards_str = get_names(film.get('awards', []), awards)
        film_types_str = get_names(film.get('types', []), types)
        film_languages_str = get_names(film.get('languages', []), languages)
        film_countries_str = get_names(film.get('countries', []), countries)

        # Construct the film URL
        base_url = 'https://sitgesfilmfestival.com'
        film_url_path = film.get('url', {}).get('en', '')
        film_url = base_url + film_url_path

        # Scrape the director's name and biography
        try:
            response = requests.get(film_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Find the director's name
                director_div = soup.find('div', id='sff-film-directors')
                if director_div:
                    director_name_tag = director_div.find('div', class_='field--name-node-title')
                    if director_name_tag:
                        director_name = director_name_tag.get_text(strip=True)
                    else:
                        director_name = ''
                    # Find the director's biography
                    bio_tag = director_div.find('div', class_='field--name-field-multi-biography')
                    if bio_tag:
                        director_bio = bio_tag.get_text(strip=True)
                    else:
                        director_bio = ''
                else:
                    director_name = ''
                    director_bio = ''
            else:
                director_name = ''
                director_bio = ''
        except Exception as e:
            director_name = ''
            director_bio = ''

        # Prepare the row
        row = [
            session_id,
            session_start,
            session_end,
            session_duration,
            session_location,
            session_talent,
            session_qa,
            session_day,
            film_id,
            film_international_title,
            film_original_title,
            film_year,
            film_duration,
            director_name,
            director_bio,
            film_synopsis,
            film_credits,
            film_genres_str,
            film_sections_str,
            film_categories_str,
            film_awards_str,
            film_types_str,
            film_languages_str,
            film_countries_str,
            film_url
        ]
        rows.append(row)

# Write to CSV file
with open('composite_sessions.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print("CSV file 'composite_sessions.csv' has been generated successfully.")
