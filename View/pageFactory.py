from enum import Enum


# this is a simple factory pattern
# used to get the page template based on the page type
class PageType(Enum):
    HOME = "home.html"
    ABOUT = "about.html"
    CONTACT = "contact.html"


# this factory class is used 
# to get the page template based on the page type defined in the PageType enum
class PageFactory:
    @staticmethod

    def get_page(page_type: PageType , is_partial : bool = False):

        prefix = "partials/" if is_partial else ""
        return prefix + page_type.value