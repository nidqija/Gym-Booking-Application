from Model.sessions import Session


class HomeService:
    @staticmethod
    def get_home_data(current_user):
       display_name = current_user.full_name if current_user else "Guest"
       print(f"DEBUG: Current user is {display_name} ({current_user.email if current_user else 'No email'})")


       all_sessions = Session.get_all_sessions()
       print(f"DEBUG: Retrieved {len(all_sessions)} sessions from the database.")
        
       return {
           "display_name": display_name,
           "all_sessions": all_sessions
       }