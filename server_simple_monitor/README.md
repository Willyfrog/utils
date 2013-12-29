server simple monitor
=====

Simple, quick and dirty script I use to monitor my websites.

requirements:
- python 2.7
- requests

Just change in the config the urls you want to monitor and 
the email config to use for alerts

Two conditions will trigger email alerts:
- server response code for any url is not 200
- server response content for any url does not contain a given text
  ( so server is responding 200 and dynamic content is served )

Add this script to your crontab as often as you need.

this script is unlicensed 
