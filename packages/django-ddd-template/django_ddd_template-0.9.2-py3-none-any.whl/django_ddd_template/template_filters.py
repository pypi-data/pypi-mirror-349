from django.template import Engine


def register_custom_filters():
    engine = Engine.get_default()

    # Conversión de casos
    engine.filters['snake_case'] = lambda x: x.lower().replace(' ', '_')
    engine.filters['camel_case'] = lambda x: x.title().replace(' ', '').replace('_', '')
    engine.filters['kebab_case'] = lambda x: x.lower().replace(' ', '-').replace('_', '-')

    # Para nombres de archivos
    engine.filters['file_name'] = lambda x: x.lower().replace(' ', '_')

    # Para nombres de variables
    engine.filters['var_name'] = lambda x: x.lower().replace(' ', '_').replace('-', '_')

    # Pluralización simple
    engine.filters['plural'] = lambda x: x + 's' if not x.endswith('s') else x