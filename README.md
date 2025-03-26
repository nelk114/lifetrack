# lifetrack

A Habit Tracking Web App.
Primarily for University Coursework purposes.
More info to be added by someone more eloquent than I.

Requires Python & Django
(building and testing against versions 3.11 and 2.2.28 respectively).
The relevant Django version (and subsidiary libs)
are documented in `requirements.txt`;
installing them should only require
`pip install -r requirements.txt`
assuming you have `pip` installed.

To actually run anything you'll need to make the db migrations
(they're intentionally excluded from comitting as they're autogenerated):
in the project's basedir
(& with the relevant virtualenv active)
do
`python manage.py makemigrations` then `python manage.py migrate`.
Obviously as developm't continues
this'll only be necessary if the models change
(or if reïnstalling fsr)

Since `DEBUG` mode is off,
`python manage.py runserver`
won't serve static files;
apparently it expects that to be done by the (‘proper’) webserver.
`python manage.py runserver --insecure` will bypass this though.
