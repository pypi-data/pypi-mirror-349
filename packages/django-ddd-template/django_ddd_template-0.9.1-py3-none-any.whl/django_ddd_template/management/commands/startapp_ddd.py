import os
import shutil
from django.core.management.base import BaseCommand, CommandError
from string import Template
from django_ddd_template.templates_registry import TEMPLATES


class Command(BaseCommand):
    help = "Create a Django app with a DDD structure and initial implementation"

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str)
        parser.add_argument("--base-url", type=str, default=None,
                            help="Custom base URL for the API endpoints")

    def handle(self, *args, app_name=None, **kwargs):
        if not app_name:
            raise CommandError("You must provide an app_name")

        base_path = os.getcwd()
        target_path = os.path.join(base_path, app_name)
        template_structure_path = os.path.join(os.path.dirname(__file__), "../../templates/ddd_app")

        if os.path.exists(target_path):
            raise CommandError(f"The folder '{app_name}' already exists.")

        # 1. Copiar estructura de carpetas
        shutil.copytree(template_structure_path, target_path)

        # 2. Preparar contexto para las plantillas
        context = {
            "app_name": app_name.lower(),
            "AppName": app_name.capitalize(),
            "base_url": kwargs.get('base_url') or f"{app_name.lower()}s"
        }

        # 3. Procesar plantillas desde el diccionario TEMPLATES
        for rel_path, template_content in TEMPLATES.items():
            dest_path = os.path.join(target_path, rel_path)

            # Asegurar que existe el directorio destino
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            # Procesar la plantilla con las sustituciones
            template = Template(template_content)
            processed_content = template.safe_substitute(context)

            # Escribir archivo resultante
            with open(dest_path, "w") as f:
                f.write(processed_content)

        self.stdout.write(self.style.SUCCESS(f"App '{app_name}' created with DDD structure and implementation"))