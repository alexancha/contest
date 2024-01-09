from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from contest.models import Mootcourt
from contest.permissions import IsOrganizerOrReadOnly
from contest.seriallizers import MootcourtSerializer
from users.models import Team


class MootcourtViewSet(viewsets.ModelViewSet):

    queryset = Mootcourt.objects.all()
    serializer_class = MootcourtSerializer
    permission_classes = [IsOrganizerOrReadOnly]

    def finish_mootcourt(self, request):
        # rating_data = request.data.get('team_rating')
        # team_id = request.data.get('team_id')
        rating_data = request.data.get('team_ratings')
        print(request.data)
        for team_id, rating in rating_data.items():
            team = Team.objects.get(pk=team_id)
            team.rating = (team.rating + rating)/2
            team.save()

        return Response({'message': 'Mootcourt finished successfully'}, status=status.HTTP_200_OK)
