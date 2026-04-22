from enum import Enum

# 1. Factory Pattern 
# this is a simple factory pattern
# used to get the page template based on the page type
class PageType(Enum):
    HOME = "home.html"
    SCHEDULE = "booking.html"


# this factory class is used 
# to get the page template based on the page type defined in the PageType enum
class PageFactory:
    @staticmethod
    def get_page(page_type: PageType , is_partial : bool = False):
        # if is_partial is true then we return the partial page template path
        prefix = "partials/" if is_partial else ""
        return prefix + page_type.value