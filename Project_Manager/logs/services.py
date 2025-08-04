from logs.models import ActionLog



def log_action(action, user, data=None, team=None, project=None, task=None):
    print('LOGGING:', action, '| user:', user, '| team:', team, '| project:', project)
    ActionLog.objects.create(
        user=user,
        project=project,
        team=team if team is not None else project.team,
        action_type=action,
        data=data
    )