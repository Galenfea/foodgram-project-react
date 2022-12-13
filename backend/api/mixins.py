from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from core.messages import ERRORS

class CreateListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet
                        ):
    pass


class CreateRetriveDeleteViewSet(mixins.CreateModelMixin, 
                                 mixins.RetrieveModelMixin,
                                 mixins.DestroyModelMixin,
                                 viewsets.GenericViewSet
                                 ):
    pass


class CreateDeleteMixin:
    '''Миксин класс для добавления и удаления объектов в таблицах m2m.'''
    def create_delete(self, request, model, field, pk=None):
        print('CREATE_DELETE_BEGIN')
        object = get_object_or_404(self.queryset, pk=pk)
        print('Что за объект?', object)
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        kwargs = {'user': user, field: object}
        if request.method == 'POST':
            try:
                model.objects.create(**kwargs)
            except:
                raise ValidationError(
                    ERRORS['CREATE_DELETE_MIXIN_IS_RELATIONS']
                )
            # Методы будут доступны в классе, наследуемом от ModelViewSet
            serializer_class = self.get_serializer_class()
            print('SERIALIZER CLASS: ', serializer_class)

            context = self.get_serializer_context()
            serializer=serializer_class(object, context=context) 
            print('DATA СЕРИАЛАЙЗЕР: ', serializer.data)
            response = Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )

        if request.method == 'DELETE':
            try:
                models_object = get_object_or_404(model.objects.filter(**kwargs))
                print(models_object)
                models_object.delete()
            except:
                raise ValidationError(
                    ERRORS['CREATE_DELETE_MIXIN_NO_RELATIONS']
                ) 
            response = Response(status=status.HTTP_204_NO_CONTENT)
            print('CREATE_DELETE_END')

        return response
