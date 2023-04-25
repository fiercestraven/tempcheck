
<!-- https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax -->


# TEMPCHECK
![Thermometer logo for Tempcheck](https://favpng.com/png_view/clip-art-transparency-thermometer-png/zmfJtM6h)
Tempcheck is a web app designed to help instructors track how well students are understanding a lecture by providing a simple interface for students to ping and visual feedback for instructors and students.

This is the software piece of the capstone dissertation project for the completion of the MSc in Software Development at Queen's University Belfast in 2023.

## FEATURES
-Non-intrusive
-Supports in-person or virtual lectures
-Applicable in other settings, such as lab sessions
-Customisation options available
-Statistical analysis for instructors

## OVERVIEW
Academic lectures are often given to large groups of students, increasingly in an online environment. These two factors make it difficult for instructors to gauge the reaction of students to the material, and for students to sense the overall understanding of the material by their peers. Traditional solutions, such as online polls, showing hands, or physical notecards are all fairly intrusive and are more difficult to implement in an online environment.

Tempcheck is a web app designed to be minimall intrusive to students and instructors alike. Student log in to a web app and have the opportunity to "ping" at any point in the lecture. Instructors have the ability to pre-set threshold levels according to their comfort. When the number of pings in a 2-minute time frame passes a threshold, an icon of a thermometer on the web app changes colour, slowly "heating up" from green to yellow to orange to red. An optional smart lightbulb can be connected to the lecture in order to provide a more ambient visual indicator of the mood of the class. 

Tempcheck is designed to be flexible. Instructors can adjust their threshold settings, choose whether to include a lightbulb, and reset the temperature at any time during the lecture. While Tempcheck is designed to be used in lectures, it works equally well in other settings, such as a group lab session.

### BATCH USER UPLOAD VIA CSV
There is a csv file upload available through the Django admin interface to facilitate batch importing student and/or staff data. This file must be of type .csv and should follow either of the following formats:
username,first_name,last_name,email,is_staff
username,first_name,last_name,email,password,is_staff
*please note that in the second instance above, assigned passwords may not contain any comma ',' characters. 

### PASSWORD RECOMMENDATIONS
User passwords are recommended to be between 8-20 characters and contain at least one number and one uppercase letter.

## DEMO
<!-- fv link to video here -->

## TESTS
<!-- fv Provide examples on how to run them here. -->

## FUTURE FEATURES
<!-- fv list improvements here -->

## BUILT WITH
<!-- fv check this with Dan -->
Django / Python
Next.js / React / JavaScript
HTML
CSS

## ACKNOWLEDGEMENTS

Many thanks to Aidan McGowan, supervisor and mentor for this project. Thanks also to Queen's University Belfast.

## FEEDBACK/CONTACT

[Frances Veit](fveit01@qub.ac.uk)

## LICENSE
Licensed under the [MIT](https://github.com/microsoft/vscode/blob/main/LICENSE.txt) license.