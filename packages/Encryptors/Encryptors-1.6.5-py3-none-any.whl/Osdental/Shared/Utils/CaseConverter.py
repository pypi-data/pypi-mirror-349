import re

class CaseConverter:
    
    @staticmethod
    def case_to_snake(name: str) -> str:
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    @staticmethod
    def snake_to_camel(snake_str: str) -> str:
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])
    
    @staticmethod
    def snake_to_pascal(snake_str: str) -> str:
        components = snake_str.split('_')
        return ''.join(x.title() for x in components)