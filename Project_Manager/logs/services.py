from logs.models import ActionLog

def log_action(action, user, data=None, task=None, project=None, team=None):

    if project is None and task is not None:
        project = task.project
    
    if team is None:
        if project is not None and project.team is not None:
            team = project.team
        elif task is not None and task.project is not None and task.project.team is not None:
            team = task.project.team
        else:
            team = None
    

    log = ActionLog.objects.create(
        user=user,
        task=task,
        project=project,
        team=team,
        action_type=action,
        data=data or {}
    )

    practicants = set()
    
    if team:
        practicants.update(team.team_member.all())
    
    if project and hasattr(project, 'pm'):
        pm_users = project.pm.all().values_list('user_id', flat=True)
        practicants.update(pm_users)
    

    practicants.add(user.id)
    
    log.participants.set(practicants)
    
    return log