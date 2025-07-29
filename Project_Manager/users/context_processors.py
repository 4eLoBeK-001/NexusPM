from .models import Notifications
from teams.models import TeamInvitation


def tracker_unread_notifications_processor(request):
    unread_notifications = Notifications.objects.filter(user=request.user.is_authenticated, is_read=False).count()
    unread_invitations = TeamInvitation.objects.filter(invited_user=request.user.is_authenticated, accepted=False).count()
    return {
        'unread_notifications': unread_notifications + unread_invitations
    }