from rest_framework import mixins
from rest_framework import viewsets


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