Fortune Speak
=============

Fortune Speak is a Python sample app for Managed VMs that synthesize and display a random fortune sound everytime you load the page.

[Demo](http://fortunespeak.appspot.com/)

It extends a traditional Python App Engine application with new
functionalities that are unlocked by Managed VMs
- *Get more CPU and RAM* by running your App Engine module on Google Compute Engine VMs
    - set GCE machine type in `app.yaml` ([view sources](https://github.com/GoogleCloudPlatform/appengine-vm-fortunespeak-python/blob/0c65d79e278dd31df837f70d85c563e4dc15e52b/app.yaml#L10))
- *Escape the sandbox* by writing to files and launching subprocess
    - cache wave file to local disk ([view sources](https://github.com/GoogleCloudPlatform/appengine-vm-fortunespeak-python/blob/0c65d79e278dd31df837f70d85c563e4dc15e52b/main.py#L43))
    - launch the `fortune` executable ([view sources](https://github.com/GoogleCloudPlatform/appengine-vm-fortunespeak-python/blob/0c65d79e278dd31df837f70d85c563e4dc15e52b/main.py#L36))
- *Customize your runtime* by installing third party packages
    - install the `fortune` package with `apt-get` ([view sources](https://github.com/GoogleCloudPlatform/appengine-vm-fortunespeak-python/blob/0c65d79e278dd31df837f70d85c563e4dc15e52b/Dockerfile#L5))
    - install `pyttsx` and `flask` from [`requirements.txt`](https://github.com/GoogleCloudPlatform/appengine-vm-fortunespeak-python/blob/0c65d79e278dd31df837f70d85c563e4dc15e52b/requirements.txt) with `pip` ([view sources](https://github.com/GoogleCloudPlatform/appengine-vm-fortunespeak-python/blob/0c65d79e278dd31df837f70d85c563e4dc15e52b/Dockerfile#L7))
- *Call into native* Python C extensions
    - import and call `_speak` `pyttsx` driver ([view sources](https://github.com/GoogleCloudPlatform/appengine-vm-fortunespeak-python/blob/0c65d79e278dd31df837f70d85c563e4dc15e52b/synth.py#L11))

Below is a tutorial that will guide you on how to build, run and deploy this application step by step.

## Prerequisites

During this step you will
- create a new Managed VMs project
- provision your local development environments
- run the final application locally and deploy it to production

### Create your project

1. Go to [Google Developers Console](//cloud.google.com/console) and create a new project.
2. Enable billing
3. Open `https://preview.appengine.google.com/settings?&app_id=s~<project>`
4. Click `Setup Google APIs project for VM Runtime...`

### Setup Docker

1. Install boot2docker
    - [MacOSX](http://docs.docker.io/installation/mac/) instructions
    - [Windows](http://docs.docker.io/installation/windows/) instructions
    - [Linux](https://github.com/boot2docker/boot2docker-cli/releases) releases
2. Setup and start boot2docker

        boot2docker init
        boot2docker up

### Setup the Cloud SDK

1. Get and install the SDK preview release
2. Setup the Managed VMs components:
        gcloud components update appengine-managed-vms
        gcloud auth login
        gcloud set project <project>
        docker pull gcr.io/google_appengine/python-compat

### Run the application locally

1. Get the application code

        git clone https://github.com/GoogleCloudPlatform/appengine-vm-fortunespeak-python
        cd appengine-vm-fortunespeak-python
        git fetch --all

2. Run the application locally

        gcloud preview app run app.yaml

3. After seeing a request to `/_ah/start` in the logs open [http://localhost:8080](http://localhost:8080)


### Deploy the application to your project
      
1. Build and deploy the application image

        gcloud preview app deploy app.yaml --server preview.appengine.google.com

2. After the command complete succesfully open `https://<project>.appspot.com`

## Hello World!

During this step you will:
- create a simple Python hello world application

0. First switch to `step0` branch

        git checkout step0

1. Create a `app.yaml` file w/ the default App Engine configuration
2. Create a `main.py` file using `webapp2` w/ a `RequestHandler` that print `hello: <Country the HTTP request is coming from>`
3. Run locally and deploy it to production.

### Solution

- Review the [solution](https://github.com/GoogleCloudPlatform/appengine-vm-fortunespeak-python/compare/proppy:step0...step1)
- Compare with your working directory

        git diff step1 -R

- If stuck, stash your working directory and switch to the solution branch

        git stash
        git checkout step1

## Hello Managed VMs

During this step you will:
- enable Managed VMs in your application configuration
- select a bigger instance class

1. Modify `app.yaml` to add `vm: true` 
2. Modify `app.yaml` to select a bigger instance class
3. Run locally
4. Notice that a Dockerfile has been created in your application directory
5. Deploy to production

### Solution

- Review the [solution](https://github.com/GoogleCloudPlatform/appengine-vm-fortunespeak-python/compare/proppy:step1...step2)
- Compare with your working directory

        git diff step2 -R

- If stuck, stash your working directory and  switch to the solution branch

        git stash
        git checkout step2

## Escape the sandbox

During this step you will:
- perform system operation: write to the local filesystem

1. Modify `main.py` to log the greetings to a file called 'messages.txt'
2. Modify `main.py` to add a new `RequestHandler` that display the content of this file.
3. Run locally and deploy it to production

### Solution

- Review the [solution](https://github.com/GoogleCloudPlatform/appengine-vm-fortunespeak-python/compare/proppy:step2...step3)
- Compare with your working directory

        git diff step3 -R

- If stuck, stash your working directory and switch to the solution branch

        git stash
        git checkout step3

## Customize the Runtime Environment

During this step you will:
- add native dependencies to your application with `apt-get`
- perform system operattion: launch an external process

1. Modify `Dockerfile` to `RUN apt-get install -y fortunes`
2. Modify `main.py` to launch `/usr/games/fortunes`  with the `subprocess` module in the main `RequestHandler`, capture the standard output and display it back in the response.
3. Run it locally and deploy to production

### Solution

- Review the [solution](https://github.com/GoogleCloudPlatform/appengine-vm-fortunespeak-python/compare/proppy:step3...step4)
- Compare with your working directory

        git diff step4 -R

- If stuck, stash your working directory and switch to the solution branch

        git stash
        git checkout step4

## Manage Python dependencies

During this step you will:
- managed your application dependencies with `pip` and `requirements.txt`
- rewrite your web application handler using a modern python framework `Flask`

1. Create a `requirements.txt` with `Flask` listed as a dependency
2. Modify `Dockerfile` to `RUN pip install -r requirements.txt -t .`
3. Edit `main.py` to use `flask.route` instead of `webapp2.RequestHandler`
4. Run it locally and deploy to production

### Solution

- Review the [solution](https://github.com/GoogleCloudPlatform/appengine-vm-fortunespeak-python/compare/proppy:step4...step5)
- Compare with your working directory

        git diff step5 -R

- If stuck, stash your working directory and switch to the solution branch

        git stash
        git checkout step5

## Use Python C extensions

During this step you will:
- add `pyttsx` C extensions as a dependency of your application
- call into native code to perform text to speech.

1. Modify `requirements.txt` to list `pyttsx` as a depdency
2. Copy the file `synth.py` from the master branch

        git checkout master synth.py

3. Call `synth.Say` from you main request handler and return the wavform data with the `audio-x/wav` content type
4. Run it locally and deploy to production

### Solution

- Review the [solution](https://github.com/GoogleCloudPlatform/appengine-vm-fortunespeak-python/compare/proppy:step5...step6)
- Compare with your working directory

        git diff step6 -R

- If stuck, stash your working directory and switch to the solution branch

        git stash
        git checkout step6
