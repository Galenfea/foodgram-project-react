from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from core.messages import ERRORS


class CreateDeleteMixin:
    '''Миксин класс для добавления и удаления объектов в таблицах m2m.'''
    def create_delete(self, request, model, field, pk=None):
        object = get_object_or_404(self.queryset, pk=pk)
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        kwargs = {'user': user, field: object}
        if request.method == 'POST':
            try:
                model.objects.create(**kwargs)
            except IntegrityError:
                raise ValidationError(
                    ERRORS['CREATE_DELETE_MIXIN_IS_RELATIONS']
                )
            # Методы будут доступны в классе, наследуемом от ModelViewSet
            serializer_class = self.get_serializer_class()
            context = self.get_serializer_context()
            serializer = serializer_class(object, context=context)
            response = Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )

        if request.method == 'DELETE':
            try:
                models_object = get_object_or_404(
                    model.objects.filter(**kwargs)
                )
                models_object.delete()
            except Http404:
                raise ValidationError(
                    ERRORS['CREATE_DELETE_MIXIN_NO_RELATIONS']
                )
            response = Response(status=status.HTTP_204_NO_CONTENT)

        return response
