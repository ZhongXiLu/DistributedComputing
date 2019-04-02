To run the angular application install anngular on your machine using node command line (https://angular.io/guide/quickstart).
Once you have angular installed go to DistributedComputing/front-end/frontend/ and run:

npm install
ng serve

The application should run on port 4200
if you want to go to the login page go to localhost:4200/login
and login using angela as both the password and the username.
Before you login you should also run the flask backend by running
 
python run.py

The run.py file is in DistributedComputing/front-end/project/
If you look into the DistributedComputing/front-end/frontend/src/app/login/login.component.ts
you will see the call to the login api. It looks like something below:

this.http.post('http://127.0.0.1:5000/api/users/token', {
      username: username,
      password: password
    })

All the api are in this folder:
DistributedComputing/front-end/project/api/api.py