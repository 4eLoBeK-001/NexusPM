from logs.models import ActionLog



def log_action(action, user, data=None, team=None, project=None, task=None):
    ActionLog.objects.create(
        user=user,
        team=team or (project.team if project else None),
        project=project,
        action_type=action,
        data=data
    )