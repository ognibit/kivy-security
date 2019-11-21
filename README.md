# kivy-security
A security framework for Python Kivy

## Features
The project aims to have all these features:
* don't set any constraints in terms of UX. The only exception is the need of a
  login screen and a action to logout;
* interchangeable authentication service;
* interchangeable authorization service;
* interchangeable audit service;
* ACLs based on user roles;
* works only is single user mode;
* configuration via code, file and settings panel;

All the features are not already implemented. Check the changelog of each 
release to know what is done and how.

## Changelog
See also the (releases)[https://github.com/ognibit/kivy-security/releases] on
GitHub.
### Release 0.1 
Work in progress.
* Simple configuration using python code
* Extremely simple (and not secure) AuthenticationService for the simplest
  login with user and password. 
* LoginWidget to setup the skeleton of the login page
* SecureScreen to setup an application page in secure mode
* Logut method

