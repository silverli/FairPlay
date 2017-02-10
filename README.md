# FAIR:PLAY Hackathon Repo
This project uses Django.

Before you create a workspace in Cloud9, do the steps below to make sure your SSH key is set up.

## SSH Key steps
1. In [Cloud9](https://c9.io), go to the [settings](https://c9.io/account/settings) and click on the "SSH Keys" tab.
2. Copy the ssh key and go to your Github account [settings](https://github.com/settings/profile).
3. Click on "SSH and GPG Keys", then click add "New SSH Key". Put "Cloud9" for the title and then paste in the key from Cloud9.
4. Click "Add SSH Key".
5. Next, edit or create an authorized_keys file.
6. ``` touch ~/.ssh/authorized_keys```
7. Paste in your SSH key from Cloud9, the same one that you pasted into Github.


## Getting Started
1. Create an account in Cloud9 and log in.
2. Click **Create a new workspace**. Name your workspace something like "fair-play-hackathon" whatever. 
3. In the field that says **Clone from Git or Mercurial URL**, put in ```git@github.com:silverli/FairPlay.git```
4. Under **Choose a Template**, pick "Django".

## Running your new Django app
When you run the project, you will run into errors.

Type in ``` sudo pip install psycopg2 ```

Start the database with ```sudo service postgresql start```

### Create the database

1. Type ```psql``` to open the interactive terminal for working with Postgres
2. Create a user called **fairplay** ```create user fairplay;```
3. Then do ```create database fairplay;``` to create a database called **fairplay**
4. ```alter user fairplay with password 'JmUbR3dUojwuirGk2Kls'```
5. ```alter user fairplay with superuser;```
6. To quit this terminal type ```\q```.
7. Then run ```python manage.py migrate``` to migrate your database
8. run this ```gunzip dbexport.pgsql.gz | psql fairplay``` to get the data for this hackathon
9. Upgrade Django with ```sudo pip install --upgrade Django ```

Go to https://fair-play-hackathon-anastasialanz.c9users.io/admin/
