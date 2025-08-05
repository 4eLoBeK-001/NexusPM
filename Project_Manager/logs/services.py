from logs.models import ActionLog



def log_action(action, user, data=None, task=None, project=None, team=None):
    # project = project if project is not None else None if task is None else task.project
    project = project if task is None else task.project
    log = ActionLog.objects.create(
        user=user,
        task=task,
        project=project,
        team=team if team is not None else project.team,
        action_type=action,
        data=data
    )
    log.save()

    practicants = set()

    if team:
        practicants.update(team.team_member.all())
    
    if project:
        practicants.update(project.pm.all().values_list('user_id', flat=True))
    
    log.participants.set(practicants)