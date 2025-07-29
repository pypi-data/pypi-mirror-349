from textwrap import dedent

TEMPLATES = {
    "domain/entities/entity.py": dedent('''
        class $AppName:
            def __init__(self, id, name, description):
                self.id = id
                self.name = name
                self.description = description
    ''').strip(),

    "domain/repositories/entity_repository.py": dedent('''
from abc import ABC, abstractmethod

class $AppNameRepository(ABC):
    @abstractmethod
    def get_by_id(self, entity_id): pass

    @abstractmethod
    def save(self, entity): pass
''').strip(),

    "domain/services/entity_service.py": dedent('''
from $app_name.domain.entities.entity import $AppName

class $AppNameService:
    def __init__(self, repository):
        self.repository = repository

    def register_entity(self, name, description):
        entity = $AppName(None, name, description)
        return self.repository.save(entity)
''').strip(),

    "infrastructure/models/entity_model.py": dedent('''
from django.db import models

class $AppNameModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
''').strip(),

    "infrastructure/repositories/django_entity_repository.py": dedent('''
from $app_name.domain.entities.entity import $AppName
from $app_name.domain.repositories.entity_repository import $AppNameRepository
from $app_name.infrastructure.models.entity_model import $AppNameModel

class Django$AppNameRepository($AppNameRepository):
    def get_by_id(self, entity_id):
        model = $AppNameModel.objects.get(id=entity_id)
        return $AppName(model.id, model.name, model.description)

    def save(self, entity):
        model = $AppNameModel(name=entity.name, description=entity.description)
        model.save()
        entity.id = model.id
        return entity
''').strip(),

    "infrastructure/serializers/entity_serializer.py": dedent('''
from rest_framework import serializers
from $app_name.infrastructure.models.entity_model import $AppNameModel

class $AppNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = $AppNameModel
        fields = ['id', 'name', 'description']
''').strip(),

    "infrastructure/views/entity_view.py": dedent('''
from rest_framework import viewsets
from $app_name.infrastructure.models.entity_model import $AppNameModel
from $app_name.infrastructure.serializers.entity_serializer import $AppNameSerializer

class $AppNameViewSet(viewsets.ModelViewSet):
    queryset = $AppNameModel.objects.all()
    serializer_class = $AppNameSerializer
''').strip(),

    "infrastructure/urls.py": dedent('''
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from $app_name.infrastructure.views.entity_view import $AppNameViewSet

router = DefaultRouter()
router.register(r'$base_url', $AppNameViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
''').strip(),

    "tests/test_entity_service.py": dedent('''
import unittest
from $app_name.domain.services.entity_service import $AppNameService
from $app_name.domain.entities.entity import $AppName

class InMemory$AppNameRepository:
    def __init__(self):
        self.data = {}
        self._id_counter = 1

    def get_by_id(self, entity_id):
        return self.data.get(entity_id)

    def save(self, entity):
        entity.id = self._id_counter
        self.data[self._id_counter] = entity
        self._id_counter += 1
        return entity

class $AppNameServiceTestCase(unittest.TestCase):
    def test_register_entity(self):
        repo = InMemory$AppNameRepository()
        service = $AppNameService(repo)

        entity = service.register_entity("Example", 'description')

        self.assertIsNotNone(entity.id)
        self.assertEqual(entity.name, "Example")
        self.assertEqual(entity.description, 'description')

if __name__ == '__main__':
    unittest.main()
''').strip(),
}
