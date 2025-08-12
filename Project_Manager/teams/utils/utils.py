from django.shortcuts import get_object_or_404, redirect, render
from teams.models import Team

def redirect_back(request, fallback='teams:team_list'):
    return redirect(request.META.get('HTTP_REFERER', fallback))


def get_team_and_redirect(request, pk):
    response = redirect(request.META.get('HTTP_REFERER'))
    team = get_object_or_404(Team, pk=pk, team_member=request.user)
    if request.GET.get('trigger') == 'detail':
        response = redirect('teams:team_list')
    return team, response


PERMISSION_LABELS = {
    'can_delete_team': 'Может удалить команду',
    'can_change_team': 'Может изменить команду',
    'can_change_role': 'Может изменять роли',
    'can_delete_team_members': 'Может удалять участников команды',
    'can_send_invitation': 'Может приглашать участников',

    'can_create_project': 'Может создать проект',
    'can_delete_project': 'Может удалить проект',
    'can_change_project': 'Может изменить проект',
    'can_change_status_project': 'Может изменять статус проекта',
    'can_delete_project_members': 'Может удалить участника проекта',
    'can_add_project_members': 'Может добавлять участников проекта',
    'can_create_tag': 'Может создавать теги',
    'can_delete_tag': 'Может удалять теги',
    'can_create_status': 'Может создавать статусы',
    'can_delete_status': 'Может удалять статусы',

    'can_create_tasks': 'Может создавать задачи',
    'can_change_tasks': 'Может изменять задачи',
    'can_delete_tasks': 'Может удалять задачи',
    'can_change_status_task': 'Может изменять статус задачи',
    'can_change_priority_task': 'Может изменять приоритет задачи',
    'can_add_image_task': 'Может прикреплять изображения к задаче',
    'can_create_subtasks': 'Может создавать подзадачи',
    'can_assign_tag_tasks': 'Может назначать теги задачам',
    'can_add_executor_tasks': 'Может назначать исполнителей задач',
    'can_add_comment': 'Может оставлять комментарии',
    'can_delete_comment': 'Может удалять комментарии',
}

ROLE_PERMISSIONS = {
    'Creator': {
        'can_delete_team': True,
        'can_change_team': True,
        'can_change_role': True,
        'can_delete_team_members': True,
        'can_send_invitation': True,

        'can_create_project': True,
        'can_delete_project': True,
        'can_change_project': True,
        'can_change_status_project': True,
        'can_delete_project_members': True,
        'can_add_project_members': True,
        'can_create_tag': True,
        'can_delete_tag': True,
        'can_create_status': True,
        'can_delete_status': True,

        'can_create_tasks': True,
        'can_change_tasks': True,
        'can_delete_tasks': True,
        'can_change_status_task': True,
        'can_change_priority_task': True,
        'can_add_image_task': True,
        'can_create_subtasks': True,
        'can_assign_tag_tasks': True,
        'can_add_executor_tasks': True,
        'can_add_comment': True,
        'can_delete_comment': True,
    },
    'Admin': {
        'can_delete_team': False,
        'can_change_team': True,
        'can_change_role': True,
        'can_delete_team_members': True,
        'can_send_invitation': True,

        'can_create_project': True,
        'can_delete_project': True,
        'can_change_project': True,
        'can_change_status_project': True,
        'can_delete_project_members': True,
        'can_add_project_members': True,
        'can_create_tag': True,
        'can_delete_tag': True,
        'can_create_status': True,
        'can_delete_status': True,

        'can_create_tasks': True,
        'can_change_tasks': True,
        'can_delete_tasks': True,
        'can_change_status_task': True,
        'can_change_priority_task': True,
        'can_add_image_task': True,
        'can_create_subtasks': True,
        'can_assign_tag_tasks': True,
        'can_add_executor_tasks': True,
        'can_add_comment': True,
        'can_delete_comment': True,
    },
    'Manager': {
        'can_delete_team': False,
        'can_change_team': False,
        'can_change_role': False,
        'can_send_invitation': False,
        'can_delete_team_members': False,

        'can_create_project': False,
        'can_delete_project': False,
        'can_change_project': False,
        'can_change_status_project': True,
        'can_delete_project_members': False,
        'can_add_project_members': False,
        'can_create_tag': True,
        'can_delete_tag': True,
        'can_create_status': True,
        'can_delete_status': True,

        'can_create_tasks': True,
        'can_change_tasks': True,
        'can_delete_tasks': True,
        'can_change_status_task': True,
        'can_change_priority_task': True,
        'can_add_image_task': True,
        'can_create_subtasks': True,
        'can_assign_tag_tasks': True,
        'can_add_executor_tasks': True,
        'can_add_comment': True,
        'can_delete_comment': True,
    },
    'Member': {
        'can_delete_team': False,
        'can_change_team': False,
        'can_change_role': False,
        'can_send_invitation': False,
        'can_delete_team_members': False,

        'can_create_project': False,
        'can_delete_project': False,
        'can_change_project': False,
        'can_change_status_project': False,
        'can_delete_project_members': False,
        'can_add_project_members': False,
        'can_create_tag': True,
        'can_delete_tag': True,
        'can_create_status': False,
        'can_delete_status': False,

        'can_create_tasks': True,
        'can_change_tasks': True,
        'can_delete_tasks': False,
        'can_change_status_task': True,
        'can_change_priority_task': False,
        'can_add_image_task': True,
        'can_create_subtasks': True,
        'can_assign_tag_tasks': True,
        'can_add_executor_tasks': True,
        'can_add_comment': True,
        'can_delete_comment': False,
    },
    'Viewer': {
        'can_delete_team': False,
        'can_change_team': False,
        'can_change_role': False,
        'can_send_invitation': False,
        'can_delete_team_members': False,

        'can_create_project': False,
        'can_delete_project': False,
        'can_change_project': False,
        'can_change_status_project': False,
        'can_delete_project_members': False,
        'can_add_project_members': False,
        'can_create_tag': False,
        'can_delete_tag': False,
        'can_create_status': False,
        'can_delete_status': False,

        'can_create_tasks': False,
        'can_change_tasks': False,
        'can_delete_tasks': False,
        'can_change_status_task': False,
        'can_change_priority_task': False,
        'can_add_image_task': False,
        'can_create_subtasks': False,
        'can_assign_tag_tasks': False,
        'can_add_executor_tasks': False,
        'can_add_comment': True,
        'can_delete_comment': False,
    },
}


def get_role_description(role):
    descriptions = {
        'Creator': 'Имеет полный доступ к команде и проектам, назначается по умолчанию создателю команды',
        'Admin': 'Имеет полный доступ к проектам, может изменять большую часть настроек команды и проекта',
        'Manager': 'Имеет расширенный доступ к проектам: может управлять задачами и участниками внутри проектов, но не имеет доступа к настройкам команды и общим параметрам',
        'Member': 'Имеет ограниченный доступ к проекту, может создавать задачи, но не может менять настройки команды и проектов',
        'Viewer': 'Может только просматривать содержание команды и проектов. Может оставлять комментарии',
    }
    return descriptions.get(role)
