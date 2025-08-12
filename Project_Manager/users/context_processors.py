
from teams.models import TeamInvitation

# Если у пользователя появилось приглашение, то он увидет его в любой момент
def tracker_unread_invitations_processor(request):
    if request.user.is_authenticated:
        unread_invitations = TeamInvitation.objects.filter(invited_user=request.user, accepted=False).count()
        return {
            'unread_invitations': unread_invitations
        }
    return {
        'unread_invitations': TeamInvitation.objects.none()
    }