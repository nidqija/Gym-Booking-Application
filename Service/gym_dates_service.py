from Model.gymavailable import GymAvailable


class GymDatesService:
    # this function retrieves the list of blocked dates from the database and returns it as a list of strings
    # it interacts with the gymavailable model to get the data and is 
    # used by the router to display the blocked dates on the schedule page
    # router only calls this service function to get the blocked dates, it does not interact with the model directly
    @staticmethod
    def get_blocked_dates():
        gym_availability = GymAvailable.get()
        if gym_availability:
            return gym_availability.blocked_dates
        return []
    
    
    

    

