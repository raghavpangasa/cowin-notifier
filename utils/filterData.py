print("Imported Filters")

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


    def ifAvailable(self, data):
        if data["available_capacity"] > 0:
            return True
        else:
            return False


    def vaccineFilter(self, data,vaccine=""):
        if vaccine == "":
            return True
        else:
            if data["vaccine"] == vaccine:
                return True
        return False

