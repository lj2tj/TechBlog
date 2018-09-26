####Powered by python 3 and django 2.07


1. fork this project to your local
2. Clone repository to local
3. Run command: pip install -r requirements.txt(please first navigate to the same folder with requirements.txt otherwith pleasee enter full path name) to install all dependencies
4. Migrate database, run commands in same folder with manage.py:

        python manage.py makemigrations
        python manage.py migrate

5. Like step 4, create a super user:

        python manage.py createsuperuser

		
6. Before running your website, please execute PrepareWebSite.sql in mysql.

7. Like step 4 and 5, run below command to start server.

        python manage.py runserver

8. Enter url http://127.0.0.1:8000/ in browser

### contributor：
Aaron Li.
