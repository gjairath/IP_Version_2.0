# -*- coding: utf-8 -*-
"""
Created on Wed May 19 23:38:58 2021

@author: garvi
"""


#uutil stands for user-utility
#I know I'm really smart


from ip_app.models import User, Project

def find_user_obj_by_name(username):
    '''
    Params:
        username: string of the name of any user.
    Returns:
        User object associated with it.
    '''
    
    # This is safe because of the fact that the username entry is Unique.
    return User.query.filter(User.username == username).first()


def find_project_obj_by_name(project_name):
    '''
    Params:
        project_name: string of the name of any projct.
    Returns:
        Project object associated with it.
    '''
    # This is safe because of the fact that the username entry is Unique.
    return Project.query.filter(Project.project_name == project_name).first()



