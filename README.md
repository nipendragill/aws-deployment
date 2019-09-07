# Overview about repository

## Steps for api data:
- https://fylepostgres.herokuapp.com/api/v1/create/
 - Create a user first to get the token, or you can use the token that I have generate on 7th September, which will expire in 5 days
 - pass the following data in request body to create user
  - { "emailId": "abcd123@gmail.com",
      "password" : "ahgeohgaoghoa",
      "first_name" : "abcd",
      "last_name" : "def"
      }
      
      
- https://fylepostgres.herokuapp.com/api/v1/get_token/
 - After registering the user call get_token api
 - Pass following data in request body"
 - {
    "email" : "abcd123@gmail.com",
   "password": "ahgeohgaoghoa"
   }
   
   ### In below all endpoints pass, Authorization : JWT tokenobtained, content_type: application/json
   ### After this add a bank
- https://fylepostgres.herokuapp.com/api/v1/bank/
 - Pass following data in request body in json format
    {"bank_id": 47777712177,
    "name" : "AXIS"
    }
    
- https://fylepostgres.herokuapp.com/api/v1/branches/
- Add a branch with bank Id , In request body pass :
 - {
    "bank":47777712177,
	"ifsc_code":"ABCD1327",
	"branch":"WhiteField",
	"address":"Bangalore geag KR Puramgahog",
	"city":"Chennai",
	"district":"Bangalore",
	"state":"Chennai"
  }
  
- https://fylepostgres.herokuapp.com/api/v1/banks/ABCD1327/
 - Get bank details given ifsc code, hit the above url with ifsc code


- https://fylepostgres.herokuapp.com/api/v1/banks/ICICI/city_name/chennai/
 - hit the above url with bank_name and city_name in query params, Pass bank name without space separated like for AXIS BANK pass AXIS
 
 - for paginated response 
 - hit the url below
 - https://fylepostgres.herokuapp.com/api/v1/banks/ICICI/city_name/chennai/?page_size=1&page=1

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
     - url(r'^banks/(?P<bank_name>[\w-]+)/city_name/(?P<city_name>[\w-]+)/?$', BankBranchDetails.as_view(), name = 'get_ifsc_bank_details')

  
## Integrated with Postgres SQL Database

# Commands to run the project

- git clone https://github.com/nipendragill/fyle_django_assignment.git
- pip install virtualenv
- virtualenv fyle_env
- Create a database with name , password, user, and set the corresponding in .env file
- run python manage.py runserver
