# Overview about repository

## Implemented User Authentication using JSon Web Tokens
- EndPoint for getting token
  - url(r'^get_token/$', authenticate_user, name='get_token')
  - Token expiry date is set to 5 days
  
## Implemented Pagination based response
- Page Size is set to be 10

## Modified Inbuilt User Model provided by Django by AbstractBaseUser where user could attach extra required fields
- EndPoint for create user and get all the users
  - url(r'^create/$', CreateUserAPIView.as_view(), name='create_user')
 
 - EndPoint for adding a bank and get details of all banks(allowed methods, [GET,POST])
  - url(r'^bank/$', BankAPIView.as_view(), name='bank_info')
  
  - EndPoint for adding a bank and get all branches (allowed methods, [GET, POST])
    - url(r'^branches', BranchesView.as_view(), name='add_branch')
   
   - EndPoint for getting bank details given IFSC code (allowed methods , [GET])
    - url(r'^banks/(?P<ifsc_code>[\w-]+)/?$', BankIFSCDetails.as_view(), name = 'ifsc_bank_info')
    
   - EndPoint for list of all banks given city name and bank name(allowed methods,[GET])
    -     url(r'^banks/(?P<bank_name>[\w-]+)/city_name/(?P<city_name>[\w-]+)/?$', BankBranchDetails.as_view(), name = 'get_ifsc_bank_details')

  
## Integrated with MySQL Database

# Commands to run the project

- git clone https://github.com/nipendragill/fyle_django_assignment.git
- pip install virtualenv
- virtualenv fyle_env
- Go to file inside fyle_env -> Lib -> site-packages -> django ->db ->backend -> mysql -> base.py
- In base.py change , if version < (1, 3, 13): to if version < (1, 3, 12): and save
- Create a database with name , password, user, and set the corresponding in .env file
- run python manage.py runserver
