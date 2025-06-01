from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Permite acessar itens de um dicionário usando uma variável como chave no template."""
    return dictionary.get(key)
