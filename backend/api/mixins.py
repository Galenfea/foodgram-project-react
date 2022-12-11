from rest_framework import mixins
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

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
                raise ValidationError('Объект уже создан')
            # Методы будут доступны в классе, наследуемом от ModelViewSet
            serializer_class = self.get_serializer_class()
            print('SERIALIZER CLASS: ', serializer_class)

            context = self.get_serializer_context()
            serializer=serializer_class(object, context=context) 
            print('DATA СЕРИАЛАЙЗЕР: ', serializer.data)
            response = Response(data=serializer.data, status=status.HTTP_201_CREATED)
            # print('SERIALIZER CONTEXT: ', context)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)       

        if request.method == 'DELETE':
            try:
                models_object = get_object_or_404(model.objects.filter(**kwargs))
                print(models_object)
                models_object.delete()
            except:
                raise ValidationError('Объект отсутствует') 
            response = Response(status=status.HTTP_204_NO_CONTENT)
            print('CREATE_DELETE_END')

        return response
