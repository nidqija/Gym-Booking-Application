from Model.gymavailable import GymAvailable


class GymDatesService:
    @staticmethod
    def get_blocked_dates():
        gym_availability = GymAvailable.get()
        if gym_availability:
            return gym_availability.blocked_dates
        return []
    

