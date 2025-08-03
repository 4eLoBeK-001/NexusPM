from logs.models import ActionLog



def log_action(action, user, team, project, task):
    ActionLog.objects.create(
        user=user,
        team=team,
        project=project,
        action_type=action,
    )