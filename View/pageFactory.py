from enum import Enum
from abc import ABC, abstractmethod

# 1. Factory Pattern
# this is a factory pattern implementation for creating different types of dashboard pages.
# it uses an abstract class and have multiple classes
# 
class DashboardPage(ABC):
    @abstractmethod
    def get_template_path(self , is_partial : bool = False) -> str:
        pass



class HomePage(DashboardPage):
    def get_template_path(self , is_partial : bool = False) -> str:
        prefix = "partials/" if is_partial else ""
        return f"{prefix}home.html"
    

class SchedulePage(DashboardPage):
    def get_template_path(self , is_partial : bool = False) -> str:
        prefix = "partials/" if is_partial else ""
        return f"{prefix}schedule.html"


