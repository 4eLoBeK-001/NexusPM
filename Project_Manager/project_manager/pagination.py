from rest_framework.pagination import PageNumberPagination

class ExtendedPagination(PageNumberPagination):
    """
    Расширенная пагинация которая предоставляет больше страниц за раз,
    чем пагинация которая стоит по умолчанию.

    Предоставляет 50 записей на страницу.
    Ограничивает максимальное кол-во записей на одну страницу на 200
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200