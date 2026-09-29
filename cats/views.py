from rest_framework import viewsets, permissions

from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle

from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from .throttling import WorkingHoursRateThrottle

from .permisions import OwnerOrReadOnly, ReadOnly

from .models import Achievement, Cat, User

from .serializers import AchievementSerializer, CatSerializer, UserSerializer

from .pagination import CatsPagination


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = CatsPagination
    throttle_classes = (WorkingHoursRateThrottle, ScopedRateThrottle)
    throttle_scope = 'low_request'

    def get_permissions(self):
    # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернём обновлённый перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer