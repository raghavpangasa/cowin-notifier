class FilterData():
    def __init__(self):
        print("Class Imported")
    

    def paidFilter(self,data, paid=-1):
        if paid == -1:
            return True
        elif paid == 0:
            if data["fee_type"] == "Free":
                return True
            else:
                if data["fee_type"] == "Paid":
                    return True
        return False


    def ifAvailable(self, data, dose1, dose2):
        if dose1 and not dose2:
            if data["available_capacity_dose1"] > 0:
                return True
        if dose2 and not dose1:
            if data["available_capacity_dose2"] > 0:
                return True
        else:
            if data["available_capacity"] > 0:
                return True
        return False


    def vaccineFilter(self, data,vaccine=""):
        if vaccine == "":
            return True
        else:
            if data["vaccine"] == vaccine:
                return True
        return False

    def ageFilter(self, data, age18, age45):
        if age18 and not age45:
            if str(data["min_age_limit"]) == str(18):
                return True
            else:
                return False
        if age45 and not age18:
            if str(data["min_age_limit"]) == str(45):
                return True
            else:
                return False
        else:
            return True
