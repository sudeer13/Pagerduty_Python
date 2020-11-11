#!/usr/bin/env python

import argparse
import pdpyras
import sys
import csv

usersList=[]
def get_users(session):
    fields = ['UserID', 'UserName', 'Role', 'Phone', 'SMS', 'Email', 'Push'] 
    with open('Users_List.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for user in session.iter_all('users'):
            users_dict={}
            users_dict['UserID']=user['id']
            users_dict['UserName']=user['name']
            users_dict['Role']=user['role']
            for contact_method in session.iter_all('users/%s/contact_methods'%user['id']):
                if 'phone' in contact_method['type']:
                    users_dict['Phone']=contact_method['country_code'], contact_method['address']
                elif 'sms' in contact_method['type']:
                    users_dict['SMS']=contact_method['country_code'], contact_method['address']
                elif 'email' in contact_method['type']:
                    users_dict['Email']=contact_method['address']
                elif 'push_notification' in contact_method['type']:
                    users_dict['Push']=contact_method['label']
            writer.writerow(users_dict)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="Retrieves contact info for all users in a PagerDuty account")
    ap.add_argument('-k', '--api-key', required=True, help="REST API key")
    args = ap.parse_args()
    session = pdpyras.APISession(args.api_key)
    get_users(session)