# Overview about repository


## List of Curl Commands:

        1) For getting details of bank based on IFSC Code,
          query_params = ifsc_code
          You can replace the ifsc code with any one of the following [BANK1219,BANK1218,BANK1217,BANK1216,BANK1215] and run the below curl command
          curl -i 'GET' -H "Authorization":"JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2MSwidXNlcm5hbWUiOiJyeWFuY2hhdWRoYXJ5MTIzQGdtYWlsLmNvbSIsImV4cCI6MTU2ODUzODM2MywiZW1haWwiOiJyeWFuY2hhdWRoYXJ5MTIzQGdtYWlsLmNvbSJ9.4YjOUbUPeu9ZVcxKb3kFAR0yTR7ioGcEyQwH3aJ42Gc" "https://fylepostgres.herokuapp.com/api/v1/ifsc_code/?ifsc_code=BANK1219"


        2) For getting details of bank on the basis of city name and bank name
           query_params = bank_name, city_name
           Put any one of the bank name in query params[AXI BANK, CANARA BANK, STATE BANK OF INDIA]
           Please be make sure to add + , in between space like for AXIS BANK put AXIS+BANK in query bank and some for others

           Cities to search in query params [Bangalore, Chennai, Hydrebad]


        curl -X GET -H "Authorization":"JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2MSwidXNlcm5hbWUiOiJyeWFuY2hhdWRoYXJ5MTIzQGdtYWlsLmNvbSIsImV4cCI6MTU2ODUzODM2MywiZW1haWwiOiJyeWFuY2hhdWRoYXJ5MTIzQGdtYWlsLmNvbSJ9.4YjOUbUPeu9ZVcxKb3kFAR0yTR7ioGcEyQwH3aJ42Gc" "https://fylepostgres.herokuapp.com/api/v1/bank_city/?bank_name=AXIS+BANK&city_name=Bangalore"
        curl -X GET -H "Authorization":"JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2MSwidXNlcm5hbWUiOiJyeWFuY2hhdWRoYXJ5MTIzQGdtYWlsLmNvbSIsImV4cCI6MTU2ODUzODM2MywiZW1haWwiOiJyeWFuY2hhdWRoYXJ5MTIzQGdtYWlsLmNvbSJ9.4YjOUbUPeu9ZVcxKb3kFAR0yTR7ioGcEyQwH3aJ42Gc" "https://fylepostgres.herokuapp.com/api/v1/bank_city/?bank_name=STATE+BANK+OF+INDIA&city_name=Bangalore"
        curl -X GET -H "Authorization":"JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2MSwidXNlcm5hbWUiOiJyeWFuY2hhdWRoYXJ5MTIzQGdtYWlsLmNvbSIsImV4cCI6MTU2ODUzODM2MywiZW1haWwiOiJyeWFuY2hhdWRoYXJ5MTIzQGdtYWlsLmNvbSJ9.4YjOUbUPeu9ZVcxKb3kFAR0yTR7ioGcEyQwH3aJ42Gc" "https://fylepostgres.herokuapp.com/api/v1/bank_city/?bank_name=AXIS+BANK&city_name=Chennai"

        3) For getting paginated response put details same as above in point 2 along with page_size and page params

        curl -X GET -H "Authorization":"JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2MSwidXNlcm5hbWUiOiJyeWFuY2hhdWRoYXJ5MTIzQGdtYWlsLmNvbSIsImV4cCI6MTU2ODUzODM2MywiZW1haWwiOiJyeWFuY2hhdWRoYXJ5MTIzQGdtYWlsLmNvbSJ9.4YjOUbUPeu9ZVcxKb3kFAR0yTR7ioGcEyQwH3aJ42Gc" "https://fylepostgres.herokuapp.com/api/v1/bank_city/?bank_name=AXIS+BANK&page=1&page_size=2&city_name=Bangalore"
  
## Integrated with Postgres SQL Database

# Commands to run the project

- git clone https://github.com/nipendragill/fyle_django_assignment.git
- pip install virtualenv
- virtualenv fyle_env
- Create a database with name , password, user, and set the corresponding in .env file
- run python manage.py runserver
