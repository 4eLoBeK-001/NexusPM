
from teams.models import TeamInvitation


def tracker_unread_notifications_processor(request):
    unread_invitations = TeamInvitation.objects.filter(invited_user=request.user, accepted=False).count()
    return {
        'unread_invitations': unread_invitations
    }