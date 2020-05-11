# psc-library-app

This app can be viewed from https://psc-library-app.herokuapp.com/.

# Project Structure
## Endpoints:
This directory hosts all of the blueprints that are used throughout the application.
It has been broken down into two groups, `api_routes` and `view_routes`. `api_routes` host all of the endpoints to interact with the data models themselves. 
On the other hand, `view_routes` are used to host the various endpoints that return HTML templates.

## Models:
This directory hosts all of the DB models that are used to interact with the MySQL db.

## Plugins:
This directory hosts a variety of utility classes and functions that are also used throughout the application. Email, wtforms, and tokenizing is handled by these utility modules.

## Static:
This directory hosts all of javascript, css, and JSON templates that are used to make the front-end functional.

## Templates:
This directory hosts all of the Jinja2 templates that are used by the application.

# Future Improvements:
This application was written to meet the base requirements while also trying to maintain a certain level of extensibility for future development efforts. 
There is an existing column on the `users` table for group based permissions to be implemented.
A future iteration would possibly introduce the concept of an "admin" that could add books in bulk for users to "checkout".

Additionally, much of the existing modal functionality is built around a modular framework. 
Although the existing route that loads the modal is static, the concept would be to replace the `user_books` portion of the route `(/modal/user_books/<modal_type>/)` with the class of the modal that you would like to load. 
The appropriate JSON template would then be loaded, based on the passed class. 
This would then be pushed through to the Jinja2 template (as it currently functions) so that the fields are automatically created, as they currently are.

Security-wise, all of the configuration variables should be moved to environment variables and/or an un-tracked local config.json file to avoid issues when in production.
They were left within app.py to avoid issues when reviewing/attempting to run the project from a new machine.