
<!-- https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax -->


# TEMPCHECK
<!-- https://stackoverflow.com/questions/14675913/changing-image-size-in-markdown -->
<img src="tc-frontend/public/images/thermometer.png" alt="Thermometer logo for Tempcheck" width="100"/>

Tempcheck is a web app designed to help instructors track how well students are understanding a lecture. Tempcheck provides a simple interface for students to ping, along with visual feedback for instructors and students.

This is the software piece of the capstone dissertation project for the completion of the MSc in Software Development at Queen's University Belfast in 2023.

## FEATURES
- Non-intrusive
- Supports in-person or virtual lectures
- Applicable in other settings, such as lab sessions
- Customisation options available
- Statistical analysis for instructors

## OVERVIEW
Academic lectures are often given to large groups of students, increasingly in an online environment. These two factors make it difficult for instructors to gauge the reaction of students to the material, and for students to sense the overall understanding of the material by their peers. Traditional solutions, such as online polls, showing hands, or physical notecards are all fairly intrusive and are more difficult to implement in an online environment.

Tempcheck is a web app designed to be minimally intrusive to students and instructors alike. Students log in to a web app and have the opportunity to "ping" at any point in the lecture. Instructors have the ability to pre-set threshold levels according to their comfort. When the number of pings in a 2-minute time frame passes a threshold, an icon of a thermometer on the web app changes colour, slowly "heating up" from green to yellow to orange to red. An optional smart lightbulb can be connected to the lecture in order to provide a more ambient visual indicator of the mood of the class. 

Tempcheck is designed to be flexible. Instructors can adjust their threshold settings, choose whether to include a lightbulb, and reset the temperature at any time during the lecture. While Tempcheck is designed to be used in lectures, it works equally well in other settings, such as a group lab session.

## CODE OVERVIEW
Tempcheck utilises a headless architecture with a completely separate front and back end. Because the front end communicates only through the API and not directly with the database, this web app is only one possible embodiment of Tempcheck. It is poised to be implemented on other clients, such as native iOS or Android systems, using the same API.

### BACK END
Tempcheck is built on the back end with Django and Python. A customised Django-Rest-Framework API provides the endpoints necessary to run Tempcheck. The API is authenticated with a bearer token. Associated code is found in views.py, serializers.py and urls.py. 

Additionally, the back end manages and runs a site for administrative access for the database. This admin site has been customised for superusers, who have full admin privileges, and instructors, who can perform more limited tasks such as adding or editing student users; creating, modifying or deleting their own modules and lectures; setting their desired ping thresholds; and more.

The back end files consist of everything not in the tc-frontend folder and includes admin templates (such as the CSV upload tool), the system files (set aside in a folder called "tempcheck"), and the main back end production files, which are housed in a folder called "tcapp". This includes the models.py, views.py, serializers.py, and urls.py, which form the backbone of the Python/Django structure and the API.

#### BATCH USER UPLOAD VIA CSV
There is a csv file upload available through the Django admin interface to facilitate batch importing student and/or staff data. This file must be of type .csv and should follow the following format:

- username,first_name,last_name,email,is_staff

Passwords can be added through the Django interface as desired and are recommended to be between 8-20 characters and contain at least one number and one uppercase letter.


### FRONT END
The front end work is a stand-alone Next.js application and is designed to be a simple, streamlined place for students and instructors to access the necessary parts of Tempcheck. Students see a page with all of their currently active, enrolled modules. From there they can select a module and select a given lecture, where they are then given the option to ping when they are feeling stuck or confused about the lecture material.

Instructors also see their currently active modules and can select a module and lecture in order to push a button to reset the colour change any time they wish. Additionally, instructors have access to the Stats page, where they can run graphs of any module or lecture, past or present, that they have been assigned to teach. Instructors are also shown a link to the admin site, where they can access further data and perform administrative tasks to update the database.

The front end files are located in the tc-frontend folder. There are two folders that contain component pieces of pages: the Lib folder, which contains files that are pure JS, and the Component folder, which contains files whose return includes HTML. A context folder holds the auth.js file, which handles fetching and storing the user's authentication information in local storage. A pages folder holds files for the actual web pages the user encounters, while a public -> images folder holds all the images used on the site. A styles folder holds the CSS file for Tempcheck. 

It is worth noting that colour changes will happen rapidly for lectures with small enrollment numbers. If only a handful of students are registered for a module, each threshold will be reached faster than it would be with a larger class.

### LIGHTBULB
A LIFX bulb is used as an optional addition for Tempcheck and allows for more prominent visibility of the colour changes. The lightbulb can be set up at the front of a lecture hall, or positioned to be captured by a camera for online lectures. The lightbulb is currently coupled to the back end and run through the script lightbulb.py, which asks the user to select a bulb, a module, and a lecture, and then is responsive to changes in the temperature by accessing the temperature API on a loop.

## GETTING STARTED

### BACK END

Prerequisites:

- Python >= 3.10
- PostgreSQL >= 14
    With an empty database for tempcheck

Installation, from within the repository root:

1. Create a Python virtualenv: `python3 -m venv ./venv`
2. Install Python dependencies: `./venv/bin/pip install -r requirements-freeze.txt`

Configuration, editing `tempcheck/settings.py`:

1. Adjust the `DATABASES` setting to match your PostgreSQL database's `USER`, `PASSWORD`, `HOST` and `PORT`

Verify installation:

1. Run: `./venv/bin/python3 ./manage.py test`

Set up the database:

1. Apply schema migrations:  `./venv/bin/python ./manage.py migrate`
2. Create an admin user: `./venv/bin/python ./manage.py createsuperuser`

Start the server:

1. Run: `./venv/bin/python ./manage.py runserver`
2. Visit http://localhost:8000/admin/ to log into the back end admin area and manually populate data.

### FRONT END

Prerequisites:

- Node.js >= 18

Setup, from within the `tc-frontend/` directory:

1. Install the Node.js dependencies: `npm install`

Start the server:

1. Run `npm run dev`
2. Visit http://localhost:3000/ to log in and use the application.

### (OPTIONAL) SMART LIGHTBULB

Prerequisites:

- LIFX brand light with support for RGB colours.
    Connected to the same network as the Tempcheck back end server.

From the same computer as the back end server:

1. Run `./venv/bin/python ./manage.py runscript lightbulb`
2. Select a module and lecture for the lightbulb to monitor
3. When done, press ctrl-C to disconnect the lightbulb and stop the script

## DEMO
[Video demonstration](https://youtu.be/syu7XgS3O20)

## TESTING
Tempcheck includes two forms of automated testing:

1. Unit and integration testing through Django to test API access parameters
2. Web automation testing through Playwright to check for end-to-end user functionality by driving a real browser like Firefox or Chrome

Integration tests are located at tcapp/tests.py and can be run in the terminal:
> python manage.py test tcapp

Playwright tests are located in the scripts folder and all begin with test_. A simple command in the terminal will run these tests:
> pytest

## FUTURE FEATURES
- Official deployment!
- Button integration on instructor page of web app to enable lightbulb functionality
- Account maintenance for students
- Student ability to be anonymous
- Email and smart watch notifications for colour changes
- Continuous integration for bug fixes

## BUILT WITH
- Django / Python
- Next.js / React / JavaScript
- HTML
- CSS

## ACKNOWLEDGEMENTS
Many thanks to Aidan McGowan, supervisor and mentor for this project. Thanks also to Queen's University Belfast.

## FEEDBACK/CONTACT
[Frances Veit](mailto:fveit01@qub.ac.uk)

## LICENSE
Licensed under the [MIT](https://github.com/microsoft/vscode/blob/main/LICENSE.txt) license.