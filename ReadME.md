# Welcome to OpenSea, a web interface for running multi-agent RL with the pettingzoo interface

We the authors of this paper \<> (for a research seminar nothing has been published) noticed that multi-agent RL (MARL) models are programmed in a variety of programming languages (python, and C++ mainly). The current MARL training paradigm is to run models and environments with the same programming language. This has led to a distinction between python and C++ models and environments. This paradigm results in you not being able to train python, often newer, models with the, often older, C++ models. 

The fun part about MARL models is the competition. We can have different models compete directly for benchmarking, but this cannot be done if we have a stark divide between the models that can be compared in benchmarking. 

Thus we are making a simple web server to act as an environment intermediary between different models. **This will be slower than training a MARL model normally.** There is overhead in this technique, and we do address this in our paper. Though please remember our goal here isn't to make optimal latency training, but rather to allow training and benchmarking that could not previously be done without the reimplementation of models.  

---

*    [ ]  Finish & publish OpenSeaClient to pip
*    [ ]  Finish & (put somewhere?) the C++ OpenSeaClient
*    [ ]  Update Documentation

# Documentation

These guides will be broken up into categories based on programming language and client vs server-end implementations. We have one python server implementation which we decided to use to follow the most popular environment API for MARL "pettingzoo"

## Server - Python :snake: 

Our server application is located in our repository and can be used through the following:

1.   `git clone` [`https://github.com/daniel-redder/OpenSea_new.git`](https://github.com/daniel-redder/OpenSea_new.git)     
    Clone our Repository  
     
2.   `pip install -r requirements.txt`   
    Install the requirements (this was tested on python 3.10 & 3.7)  
     
3.   `python app.py`  
    To launch our flask app  
      
    **Inside app.py you will find some debug code you can use to see active environments and API-keys through the index of the webserver. We HIGHLY advise you to ensure this is off should you use this on an open port.**   
     
4.   (optional) Follow this [https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-20-04](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-20-04) or some other Flask-compatible webserver tutorial to improve the performance and security through a proper webserver configuration. In our testing we used this (nginx + uwsgi) configuration.

## Client - Python :snake: 

1.   `pip install OpenSeaClient`   
    We advise you to use pip to install this, but the code is also in "OpenSeaClient" on this repo if you want to use it directly. 

## Client - C++ :fast\_forward:
