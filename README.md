# Project Calc Pro - CS50W Capstone Project - Fernando Borea
*Read this with David Malan's voice*

Alright... this is Project Calc Pro! 

Over time I've noticed that in business, especially on new projects, having a structured way to properly identify how much a given client's project will cost can be tricky, since there are many components involved. Think of a web development agency, there may be a designer, various web developers, project managers, rented equipment, or even customer success specialists!

All those man-hours represent a cost to the business, and estimating the cost of a project can be tricky, sometimes it might be more back-end intensive, and other times it might involve heavy design and front-end work. It is crucial to be aware of how much all these efforts will cost the company.

Introducing Project Calc Pro! A cutting-edge platform that will allow businesses to save commonly used materials, their cost per unit (sometimes it might be cost per hour, other times cost per day, or per unit, and so on), to then be able to create projects. These projects will have multiple materials in various quantities, and the platform will do the heavy lifting by calculating the total project cost!

This way businesses can have project templates to quickly quote clients when they request a new job, allow for easy tracking of projects and materials, and most importantly, allow the business to focus less on the administrative tasks and more on what matters, making clients happy!

## Technical Overview and How to Run
Project Calc Pro uses Django for the back end, and Bootstrap 5 for the front end. Also, it makes use of some packages (listed on the `requirements.txt` file) to enable management of secret keys on a `.env` file for easy deployment, as well as to integrate a PostgreSQL database, allowing for ease of scalability. Note that to run this project you must install and set up PostgreSQL in your Linux instance, as well as configure the database in the `settings.py` file of the Django project. You can refer to [this article](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-20-04) for more information about how to setup PostgreSQL. Also [this article](https://django-environ.readthedocs.io/en/latest/quickstart.html) can be useful to set up `django-environ`.

## Files
- The `static/propjectcalculator` directory contains custom JavaScript scripts to enable Async requests without reloading the page.
- The `templates/projectcalculator` directory contains all the HTML files required for the user interface of the application
- The rest of the code is contained and distributed on a normal Django project structure, with a separate Python file for views, models, URLs, and dorms.
- The `requirements.txt` file contains the list of packages used for this project.
- The `.gitignore` file contains the instructions for Git about what files will be ignored for the version control.

# Distinctiveness and Complexity
Project Calc Pro is a unique Django project, very different from any other CS50W project we tackled through the course as it aims to integrate various components from them as well as create complex models and forms. Since a project contains multiple materials and each project can have various quantities of each material, it required the use of Through models to include more information about the relationship of each project instance to each material.

Also, the calculation of the total cost for each project involved the creation of custom methods inside the models to retrieve the calculation in an efficient way so it can be requested when necessary, effectively adding a new complexity layer to this programming project.

