thinkdisp
=========

Display Manager/Unity Panel Indicator for Ubuntu+Bumblebee+Multimon

This is currently experimental, but works in general unless there is an issue with the underlying Bumblebee/Nvidia/Driver setup. The usual "dev not responsible for damage to your system" applies.

Install
-------
cd into the thinkdisp folder and run the install script with
    sudo ./install
This will copy all the necessary scripts to /usr/bin/
You must already have screenclone in /usr/bin/

Usage
-----
Run
    sudo thinkdisp.py
You'll see an icon in the unity panel that controls everything


Credits
-------
The two kill scripts thinkdispk1 and thinkdispk2 are adapted from http://zachstechnotes.blogspot.com/2012/04/post-title.html
