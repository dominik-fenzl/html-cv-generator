from TemplateProvider import get_template
from strictyaml import load, Map, Str, Int, Seq, YAMLError


def start_generation():
    with open('input.yaml','r') as f:
        cv_input = load(f.read()).data

    with open('main.css', 'r') as f:
        style_sheet = f.read()

    template_values = {
        "style": style_sheet,
    }

    with open('output.html', 'w') as f:
        f.write(get_template().render(style=style_sheet, **cv_input))

if __name__ == "__main__":
    start_generation()