# How the command curl noahwilliamshaffer.com works

We call the curl command on our domain and it sends a synchronized tcp/ip request to the dns to get our servers IP. Then nginx will accept and send a response. If the server is udp then this becomes a connectionless protocol. The packets are initially sent on port 80. Then our nginx.conf will reroute the port to 443. Certbot changed niginx.conf to do this.  Now our domain that was initially on port 80 with the prefix HTTP will now be on port 443 with the prefix HTTPS. Niginix connects to gunicorn via wsgi. It works as a proxy for Gunicorn. Gunicorn invokes flask which works with the html files in the templates folder and accesses our database. This is where we pull the html from. The flask app goes back to gunicorn and then nginx. It then returns the html. 

![image.png](./image.png)
![image-1.png](./image-1.png)

## How we secure our site.

For security we will white list our ip addresses  not only from our ufw but also on nginx for making a connection to out server through ssh so that the server can only be accessed in places and computers that we find acceptable. In addition we use https which really keeps the site secure for our user.Also just by beaning aware of updates not only on digital ocean but on all of the tools we are using for hosting will help us prevent our server and site from being exploited by known zero days. We also only use ssh keys to get onto our server, and the only password is used internally to go from user to root access. Something that will be done which has not be unfortunately is to disable root logins. Using nginx is also an important part of our security because it lessens the attack surface and when it acts as a proxy it keeps the parts of the site that actually hold the files and host the site safe because only nginx is interacting with the web.


## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.


## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
for making the nginux and gunicorn server using a flask app on digital oceans use:
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-22-04

for making a auth0 login use:
https://github.com/auth0-samples/auth0-python-web-app/tree/master/01-Login

for sqlite use and getting information from your api use:
https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3


## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Authors and acknowledgment
This project was produced and develuped by Marlee Krause and Noah Shaffer

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
