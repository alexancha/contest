from rest_framework import viewsets

from users.models import Team
from users.permissions import IsOwnerOrReadOnly
from users.serializers import TeamSerializer


class TeamViewSet(viewsets.ModelViewSet):

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsOwnerOrReadOnly]
