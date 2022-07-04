from genericpath import exists
from tokenize import group

def is_user_vle(user):
    print("\n\n user is VLE \n\n")
    return user.groups.filter(name="VLE").exists()   
