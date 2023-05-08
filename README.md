
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
<!-- break this down by bits of application (back end everything but tc-frontend folder, front end everything in tc-frontend is a stand-alone next.js application, lightbulb with script) -->
<!-- completely separate back and front end communicating over api, never directly communicating with database (headless architecture) - call this out-->
<!-- web app is just one possible embodiment of this - could also do other clients, native iOS or Android using same API - call this out -->
<!-- using Django-Rest-Framework - call this out (also in report) -->
<!-- could include screenshots of file trees -->
<!-- mention that the api is authenticated with a bearer token -->
<!-- lightbulb integration currently coupled to the back end but could be implemented completely through public APIs (for report)-->

Tempcheck is built on the back end with Django and Python. It is set up in the tcapp folder and includes admin templates (such as the CSV upload tool), the system files (set aside in a folder called "tempcheck"), and the main back end production files, which are housed in a folder called "tcapp". This includes the models.py, views.py, serializers.py, and urls.py, which form the backbone of the Python/Django structure. 

The front end work, based in React/Next.js, is found in the tc-frontend folder. There are two folders that contain component pieces of pages: one is the Lib folder, which contains files that are pure JS, and the other is the Component folder, which contains files whose return includes HTML. A context folder holds the auth.js file, which handles fetching and storing the user's authentication information in local storage. A pages folder holds files for the actual web pages the user encounters, while a public -> images folder holds all the images used on the site. A styles folder holds the CSS file for Tempcheck.

## INSTALLATION AND IMPLEMENTATION
_lightbulb stuff here, too__

It is worth noting that colour changes will happen rapidly for lectures with small enrollment numbers. If only a handful of students are registered for a module, each threshold will be reached faster than it would be with a larger class.

### BATCH USER UPLOAD VIA CSV
There is a csv file upload available through the Django admin interface to facilitate batch importing student and/or staff data. This file must be of type .csv and should follow the following format:

- username,first_name,last_name,email,is_staff

Passwords can be added through the Django interface as desired and are recommended to be between 8-20 characters and contain at least one number and one uppercase letter.

## DEMO
<!-- fv link to video here -->

## TESTING
Tempcheck has two forms of automated testing set up:

1. Integration testing through Django to test API access parameters
2. Web automation testing through Playwright to check for end-to-end user functionality

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