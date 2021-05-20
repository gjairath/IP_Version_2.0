# -*- coding: utf-8 -*-
"""
Created on Wed May 19 23:38:58 2021

@author: garvi
"""


#uutil stands for user-utility
#I know I'm really smart


from ip_app.models import User

def find_user_obj_by_name(username):
    '''
    Params:
        username: string of the name of any user.
    Returns:
        User object associated with it.
    '''
    
    # This is safe because of the fact that the username entry is Unique.
    return User.query.filter(User.username == username).first()



