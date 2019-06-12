import clearbit

clearbit.key = '212c6193c089b2ce94e194efe19d36e9'

CLEARBIT = True


def clearbitCheck(email):
    if CLEARBIT:
        try:
            res = clearbit.Enrichment.find(email=email, stream=True)
            try:
                user_data = {'fullName': res['person']['name']['fullName'],
                             'givenName': res['person']['name']['givenName'],
                             'location': res['person']['location'],
                             'timeZone': res['person']['timeZone']}

                return user_data

            except:
                return False
        except:
            return False
    return False
