from django import template

register = template.Library()

@register.simple_tag
def available_page(paginator):
  all_page = []
  for x in range(1,paginator.num_pages+1):
    all_page.append(x)
  return all_page
  