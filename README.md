# Running the already deployed version

Release version availible at
https://dancingmonkeys.tech/

# Running the Application

## Frontend

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

Navigate to `src/frontend/src` to install dependencies and run the front end.

### Dependencies

For the frontend [npm (Node)](https://www.npmjs.com/get-npm) is the only dependency, all further entities used are collected with npm. 

### Installing

`npm i` to install Node dependencies.

### Available Scripts

In the frontend src directory, you can run:

#### `npm start` | `npm run start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

#### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

## Backend

### Prerequisites

Install python https://www.python.org/downloads/
If prompted to install Pip, please do so.

Open a command line tool that has python installed. 

Within the command line navigate to `src/backend/` from the root of the project

run pip install -r requirements.txt 
If successful this will install all python packages required to run the backend

### Dependencies

Specific environment variables must be set for running the API and unittests.

Within the submission there should be a .flaskenv and a .env file which will set these environment variables

When running the backend make sure that only the .flaskenv file is present in the backend folder

When running the unit tests make sure that only the .env file is present in the backend folder

### Available Scripts

To run the Backend simply run 'flask run' on the Python command line 

To run the Backend unittests run 'pytest' on the Python command line 
