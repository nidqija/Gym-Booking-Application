from enum import Enum
from abc import ABC, abstractmethod

# 1. Factory Pattern
# this is a factory pattern implementation for creating different types of dashboard pages.
# it uses an abstract class and have multiple classes
# 

# Enum to represent different page types
class PageType(Enum):
    HOME = "home.html"
    BOOKING = "booking.html"
    SIGN_IN = "signin.html"
    SIGN_UP = "signup.html"
    MY_RESERVATION = "reservation.html"

# Abstract Factory 
class PageFactory(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass


    def get_template_path(self , is_partial: bool = False) -> str:
        prefix = "partials/" if is_partial else ""
        return f"{prefix}{self.get_name().value}"
    
# Concrete Factory
class HomePage(PageFactory):
    def get_name(self) -> str:
        return PageType.HOME
    

class SchedulePage(PageFactory):
    def get_name(self) -> str:
        return PageType.BOOKING
    
    
class SignInPage(PageFactory):
    def get_name(self) -> str:
        return PageType.SIGN_IN
    

class SignUpPage(PageFactory):
    def get_name(self) -> str:
        return PageType.SIGN_UP

class MyReservationPage(PageFactory):
    def get_name(self) -> str:
        return PageType.MY_RESERVATION
    
# Creator 
class PageFactory:
    _pages = {
        PageType.HOME: HomePage,
        PageType.BOOKING: SchedulePage,
        PageType.SIGN_IN: SignInPage ,
        PageType.SIGN_UP: SignUpPage,
        PageType.MY_RESERVATION: MyReservationPage
    }

    @staticmethod
    def create_page(page_type: PageType) -> PageFactory:
        page_class = PageFactory._pages.get(page_type)
        if page_class is None:
            raise ValueError(f"Unknown page type: {page_type}")
        return page_class()
        