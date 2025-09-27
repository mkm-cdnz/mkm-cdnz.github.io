import csv
import html
import json
import re
import urllib.request
from urllib.parse import urlparse

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

RECIPES = [
    {
        'url': 'https://www.allrecipes.com/recipe/23600/worlds-best-lasagna/',
        'publication_override': 'Allrecipes',
    },
    {
        'url': 'https://www.tasteofhome.com/recipes/best-lasagna/',
        'publication_override': 'Taste of Home',
    },
    {
        'url': 'https://www.bbcgoodfood.com/recipes/classic-lasagne',
        'publication_override': 'BBC Good Food',
    },
    {
        'url': 'https://www.simplyrecipes.com/recipes/lasagna/',
        'publication_override': 'Simply Recipes',
    },
    {
        'url': 'https://www.recipetineats.com/lasagna/',
        'publication_override': 'RecipeTin Eats',
    },
]

SCRIPT_RE = re.compile(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S)


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode('utf-8', errors='ignore')


def find_recipe_node(data):
    if isinstance(data, dict):
        types = data.get('@type')
        if types == 'Recipe' or (isinstance(types, list) and 'Recipe' in types):
            return data
        for value in data.values():
            result = find_recipe_node(value)
            if result:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_recipe_node(item)
            if result:
                return result
    return None


def normalize_author(author):
    if isinstance(author, list):
        names = []
        for item in author:
            if isinstance(item, dict):
                name = item.get('name')
                if name:
                    names.append(name)
            elif isinstance(item, str):
                names.append(item)
        return ', '.join(names)
    if isinstance(author, dict):
        return author.get('name') or ''
    if isinstance(author, str):
        return author
    return ''


def normalize_publisher(publisher):
    if isinstance(publisher, dict):
        return publisher.get('name') or ''
    if isinstance(publisher, str):
        return publisher
    return ''


def parse_recipe(url: str, publication_override: str | None = None) -> dict:
    html_text = fetch(url)
    blocks = SCRIPT_RE.findall(html_text)
    recipe_data = None
    for block in blocks:
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        recipe_data = find_recipe_node(data)
        if recipe_data:
            break
    if not recipe_data:
        raise RuntimeError(f'Recipe data not found for {url}')

    description = recipe_data.get('description') or ''
    description = html.unescape(description).strip()
    description = re.sub(r'\s+', ' ', description)

    author = normalize_author(recipe_data.get('author'))
    publisher = publication_override or normalize_publisher(recipe_data.get('publisher'))
    total_time = recipe_data.get('totalTime') or ''
    yield_value = recipe_data.get('recipeYield') or ''
    if isinstance(yield_value, list):
        yield_value = ', '.join(str(v) for v in yield_value)

    date_published = recipe_data.get('datePublished') or ''
    source_domain = urlparse(url).netloc

    name = recipe_data.get('name') or recipe_data.get('headline') or ''
    name = html.unescape(name)

    return {
        'Recipe Name': name,
        'Author': author,
        'Publication': publisher or '',
        'Source': source_domain,
        'URL': url,
        'Date Published': date_published,
        'Total Time': total_time,
        'Yield': yield_value,
        'Description': description,
    }


def main():
    records: list[dict] = []
    for item in RECIPES:
        try:
            record = parse_recipe(item['url'], item.get('publication_override'))
            records.append(record)
        except Exception as exc:
            print(f"Error parsing {item['url']}: {exc}")

    fieldnames = [
        'Recipe Name',
        'Author',
        'Publication',
        'Source',
        'URL',
        'Date Published',
        'Total Time',
        'Yield',
        'Description',
    ]

    with open('datasets/lasagne_recipes.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(record)

    print(f'Wrote {len(records)} recipes')


if __name__ == '__main__':
    main()
