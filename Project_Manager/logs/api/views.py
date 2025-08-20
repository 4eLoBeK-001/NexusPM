from rest_framework import generics

from logs.api.serializers import LogActionsSerializer
from logs.models import ActionLog

class LogActionsAPIView(generics.ListAPIView):
    queryset = ActionLog.objects.all()
    serializer_class = LogActionsSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(
            participants=self.request.user
        ).select_related(
            'user', 'team', 'project', 'task'
        ).prefetch_related(
            'participants'
        ).distinct().order_by('-created_at')
        return qs