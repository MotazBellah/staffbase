
class RestAPI:
    def __init__(self, users):
        self.users = users


    def get(self, url):
        # Check if thee /users in url
        if "/users" in url:
            # Check if there is a users paramerters
            # Get the users
            parameter = url.split("?")
            if len(parameter) > 1:
                list_users = parameter[1].split("=")[1]
                exist_user = [user for user in self.users if user['name'] in list_users]
                return {'users': sorted(exist_user, key=lambda x: x["name"])}
            else:
                
                return {'users': sorted(self.users, key=lambda x: x["name"])}
        else:
            return {'error': "Not Found"}

    
    def post(self, url, payload):
        if "/add" in url:
            for user in self.users:
                if payload["user"] == user['name']:
                    return {'error': "User already exsits"}

            user_object = {
                "name": payload["user"],
                "owes": {},
                "owed_by": {},
                "balance": 0
            }
            self.users.append(user_object)
            return {'user': user_object}
        
        if "/iou" in url:
            lender = payload["lender"]
            borrower = payload["borrower"]
            amount = payload["amount"]

            lender_object = next((user for user in self.users if user["name"] == lender), False)
            borrower_object = next((user for user in self.users if user["name"] == borrower), False)

            if (not lender_object or not borrower_object):
                return {'error': "User not found"}

            if borrower in lender_object["owes"]:
                if lender_object["owes"][borrower] > amount:
                    lender_object["owes"][borrower] -= amount

                elif lender_object["owes"][borrower] < amount:
                    lender_object["owed_by"][borrower] = amount - lender_object["owes"][borrower]
                else:
                    lender_object["owes"].pop(borrower, None)
            
            else:
                if borrower in lender_object["owed_by"]:
                    lender_object["owed_by"][borrower] = lender_object["owed_by"][borrower] + amount
                else:
                    lender_object["owed_by"][borrower] = amount
            

            if lender in borrower_object["owed_by"]:
                if borrower_object["owed_by"][lender] > amount:
                    borrower_object["owed_by"][lender] -= amount

                elif borrower_object["owed_by"][lender] < amount:
                    borrower_object["owes"][lender] = amount - borrower_object["owed_by"][lender]
                else:
                    borrower_object["owed_by"].pop(lender, None)
            
            else:
                if lender in borrower_object["owes"]:
                    borrower_object["owes"][lender] = borrower_object["owes"][lender] + amount
                else:
                    borrower_object["owes"][lender] = amount
                    
            # Update the self.users
            for user in self.users:
                if user["name"] in [lender, borrower]:
                    self.users.remove(user)
            
            self.users.append(lender_object)
            self.users.append(borrower_object)

            return {'users': sorted(self.users, key=lambda x: x["name"])}






                
                



                


