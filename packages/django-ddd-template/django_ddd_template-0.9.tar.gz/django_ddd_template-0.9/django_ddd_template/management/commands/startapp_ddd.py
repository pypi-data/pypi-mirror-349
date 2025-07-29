import os
import shutil
from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
from string import Template

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
        code_template_path = os.path.join(os.path.dirname(__file__), "../../tpt")

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

        # 3. Procesar archivos .tpl para generar código fuente
        for tpl_path in Path(code_template_path).rglob("*.tpl"):
            # Convertir nombres de plantilla a estructura de directorios
            rel_path = os.path.splitext(tpl_path.relative_to(code_template_path))[0]
            rel_path = str(rel_path).replace('__', os.sep)  # domain__services → domain/services
            dest_path = os.path.join(target_path, rel_path)

            # Asegurar que existe el directorio destino
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            # Leer plantilla y aplicar sustituciones
            with open(tpl_path, "r") as f:
                template_content = f.read()

            # Usar Template de string para las sustituciones
            template = Template(template_content)
            processed_content = template.safe_substitute(context)

            # Escribir archivo resultante
            with open(dest_path, "w") as f:
                f.write(processed_content)

        self.stdout.write(self.style.SUCCESS(f"App '{app_name}' created with DDD structure and implementation"))