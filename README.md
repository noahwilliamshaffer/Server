Noah Fsu Id: nws17
Marlee Fsu Id: mmk20a
CourseNumber:Cop4342-0001
GroupNumber: 14

#Config

#whats where
Our myproject.py is our main flask project it contains all the routes for our projects. In our templates folder we have all of our html files. iOur login.html is the login page. Our signup.html is our signup page. Home.html is the defualt path after logging in. our news.html contains the articles from our database. The Admin.html will be the page our admin users are redirected to after login. Our UserProfiles.html page will have all of our users emails and names displayed as well as their associated likes with the option for the admin to delete them. Our schema.lsql is what constructs the table for all the articles to be stored and shown to the database. Our artSchema.sql has the tables in order to have each user stored with their name and email. Their email is the key that will associate them with their respective list of liked articles.Our database.db hold all the articles for printing to our news.html.Our likedArticles.db is the database where the liked articles for the respective user are stored. 
#Whats implemented and what still needs don
We have our sql database setup right now and we can succsefully store articles into our database and print them with their links to the news page. We have one data base which loads all articles for storage so we don't have to pull from hacker news every time we want to veiw them. Our actual database for the assignment is behaving correctly. It stores a user's name and email and has a list associated with each. The users email acts as a key to acsess each individuals liked articles. Once we are able to pull the users name and email we will be able to find the current sessions users and add the liked articles to the current users session email. Our admin page with be able to see the users and their all of their liked articles. We will have an array that holds admin emails and after login if the current users email is in that array they will be redirected to the admin page instead of the defualt home page. The likes and current users in session must be acsessed through a post in the html. Once we figure this part out we the rest of the implementation will be stright forward. Basically the rest of the projects implemenation depends on these posts from the html but the backend is almost complete. We will handle the admins ability to delete a post from thea user similarly to how we add a post to the user. By checking the users email and dealing with that post by it's title. 
# How the command curl noahwilliamshaffer.com works

We call the curl command on our domain and it sends a synchronized tcp/ip request to the DNS to get our server's IP. Nginx revives the packets sent by curl, accepts them, and sends back a response to complete the handshake. If the server is udp then this becomes a connectionless protocol. The packets are initially sent on port 80. Then our nginx.conf will reroute the port to 443. Certbot changed niginx.conf to do this.  Now our domain that was initially on port 80 with the prefix HTTP will now be on port 443 with the prefix HTTPS. Niginix connects to gunicorn via wsgi. It works as a proxy for Gunicorn. Gunicorn invokes flask which works with the html files in the templates folder and accesses our database. This is where we pull the html from. The flask app goes back to gunicorn and then nginx. It then returns the html to the client. 

![image.png](./image.png)
![image-1.png](./image-1.png)

## How we secure our site.

For security we will white list our ip addresses, not only from our ufw, but also on nginx for making a connection to out server through ssh so that the server can only be accessed in places and computers that we find acceptable. In addition, we use https which really keeps the site secure for our user. Also, just by being aware of updates not only on digital ocean, but on all of the tools we are using for hosting will help us prevent our server and site from being exploited by known zero days. We also only use ssh keys to get onto our server, and the only password is used internally to go from user to root access. Something that will be done which has not be unfortunately is to disable root logins. Using nginx is also an important part of our security because it lessens the attack surface and when it acts as a proxy it keeps the parts of the site that actually hold the files and host the site safe because only nginx is interacting with the web.

## How we deal with updates and upgrades
To deal with updates and upgrades we are curently using the unintended upgrades package on ubuntu to upgrade aspects of the server, it is automated and happens at random times daly. Updates and upgrades is something that we are flexable with and if we decade towrds the end of the project that unintended upgrades is not updating all the packets neccesary, we plan on implmenting ansble for updates and upgrades.

## configuration path 
 the file paths of our ssh/nginx/gunicorn/dns configuration are:

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
