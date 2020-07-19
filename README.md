# Age Prediction Server
*The current default branch is `master-tf2` (for tf-1.x support checkout the `master` branch, It's currently not in development, might have old unfiltered code.)*

*This server can be hosted on Local server or can be used with any cloud platform like AWS or GCP*

## Installing
1. Clone the repository into the desired location.
2. For linux systems install *virtualenv* to prevent breaking of the system.
    >For Ubuntu or Debian based systems run $ `sudo apt-get update && sudo apt-get install -y python3-pip && sudo pip3 install virtualenv`" 

    >For Arch linux based systems run $ `sudo pacman -Syyu && pip install --user virtualenv`
3. Use `virtualenv --python=$(which python3.7) age-prediction-server` to create the virtual environment
    >Mini-conda or Anaconda users can use `conda create -n age-prediction-server python=3.7 anaconda` (usage of python-3.7 is preferable)

    >`age-prediction-server` can be replaced with your preferred environment name.
4. Use `source <path-to-age-predicton-server>/bin/activate` to start the virtual environment
    >Mini-conda or Anaconda users use `conda activate <name-of-the-environment>`
5. Run `pip install -r requirements.txt` to install the dependencies into the environment.
6. Go to the Repository cloned location.
7. To start the server run `gunicorn --bind 0.0.0.0:5000 --workers=1 gunicorn_launch_tf2:web_app --log-level=debug`
    >You can change the bind address and port number to your desired values. Increase the number of workers if you're experiencing a lot of traffic.
8. You're Age prediction server should be up and running. Visit the webpage from the host address to verify.
9.  If running into any errors, try raising it as an issue.

## About the Server
* The server is built using the Flask micro-framework.

* The age prediction model has been trained on [IMDB faces only dataset](https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/), it is publicly available with Age, gender, etc. classes.
* The model is based on Resnet50 architecture with a custom output layer of fifteen classes and each class predicting it's respective age range.
* When tested once with random selection of 1000 images from [WIKI dataset](https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/), the model predicted with an accuracy of nearly 85%.
* The server is capable of detecting and predicting ages of multiple faces in the uploaded Image.
* Here is the Welcome page of the server.
    >![Welcome Page](https://github.com/VamsiKrishna1211/Age-Prediction/blob/master-tf2/Welcome_page.png?raw=true)
* Here is the "Results page" after predicting the ages of the faces in the image.
    >![Predction page](https://github.com/VamsiKrishna1211/Age-Prediction/blob/master-tf2/Image_prediced_page.png?raw=true)

* To run the host the website over heroku checkout my [Flask-reverse-proxy-server](https://github.com/VamsiKrishna1211/Flask-reverse-proxy-server) repository to route the traffic from heroku-platform to the Age-predictor-server (or any server) and back. (Reverse proxy server can be used to keep your main server address hidden from public eyes.)
  
*Note: Image used for prediction is obtained from "Google images"*