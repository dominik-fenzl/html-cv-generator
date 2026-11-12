import argparse

from TemplateProvider import get_template
from strictyaml import load, Map, Str, Int, Seq, YAMLError


TRANSLATIONS = {
    "de": {
        "languages": "Sprachen",
        "skills": "Developer Skills [Auszug]",
        "interests": "Interessen",
        "work_experience": "Berufserfahrung",
        "educational_path": "Bildungsweg",
        "international_experience": "Internationale Erfahrungen",
    },
    "en": {
        "languages": "Languages",
        "skills": "Developer Skills (Excerpt)",
        "interests": "Interests",
        "work_experience": "Work Experience",
        "educational_path": "Education",
        "international_experience": "International Experience",
    },
}


def start_generation(input_path='CVs/input.yaml'):
    with open(input_path,'r') as f:
        cv_input = load(f.read()).data

    with open('main.css', 'r') as f:
        style_sheet = f.read()

    language = cv_input.get('language', 'de')
    if language not in TRANSLATIONS:
        raise ValueError(f"Unknown language '{language}', expected one of: {', '.join(TRANSLATIONS)}")

    with open('output.html', 'w') as f:
        f.write(get_template().render(style=style_sheet, t=TRANSLATIONS[language], **cv_input))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate CV HTML from a YAML input file.')
    parser.add_argument('input', nargs='?', default='CVs/input.yaml',
                        help='Path to the input YAML file (default: CVs/input.yaml)')
    args = parser.parse_args()
    start_generation(args.input)