## Instructions for running the app with docker
- Install Docker (https://docs.docker.com/get-docker/)
- Clone the project with *git clone https://gitlab.com/TheRori/PMF_project.git*
- Open a terminal at the root of the project
- Run the command *docker-compose build* in terminal
- Then *docker-compose up* in terminal
- The app should be accessible at the address *localhost:8080*

## Current potential problems with docker

On MacOS for now the instructions above doesn't work because of the line
*devices:  - /dev/video0:/dev/video0* in the docker-compose file. This line should only work with Windows and Linux but it should be tested on both systems. For MacOS no solution has been found yet to get the webcam accessible from the docker.

## Instructions to install and run the app without docker

- Clone the project with *git clone https://gitlab.com/TheRori/PMF_project.git*
- Open a terminal in the repository *client*
- Run the command *npm install*
- After the end of installation run *npm run serve*
- Then open another terminal in the repsitory *server*
- Create and activate a virtual environment python (https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)
- Run the command *pip install -r requirements.txt*
- After the end of the installation run *python main.py*
- Normally the app is now ready at the address *localhost:8080*

