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


def find_project_obj_by_name(project_name, user):
    '''
    Params:
        project_name: string of the name of any projct.
        user: user object
    Returns:
        Project object associated with it.
    '''
    # This is safe because of the fact that the username entry is Unique.
    
    # User X: 1  User Y: 1
        # Which "1" to delete
    # Additional query gets the job done.
    
    # One user has many projects, in the future with TEAMS that may change into many-many.

    potential_projects = user.user_projects
        
    for pp in potential_projects:
        if (pp.author.username == user.username):
            return pp
        else:
            return None
    



