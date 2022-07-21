from genericpath import exists
from tokenize import group

def is_user_vle(user):
    print("\n\n user is VLE \n\n")
    return user.groups.filter(name="VLE").exists()   

def is_user_student(user):
    print("\n\n user is Student \n\n")
    return user.groups.filter(name="STUDENT").exists()   

def is_user_invigilator(user):
    print("\n\n user is INVIGILATOR \n\n")
    return user.groups.filter(name="INVIGILATOR").exists()   
