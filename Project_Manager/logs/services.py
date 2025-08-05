from logs.models import ActionLog



def log_action(action, user, data=None, task=None, project=None, team=None):
    # project = project if project is not None else None if task is None else task.project
    project = project if task is None else task.project
    ActionLog.objects.create(
        user=user,
        task=task,
        project=project,
        team=team if team is not None else project.team,
        action_type=action,
        data=data
    )