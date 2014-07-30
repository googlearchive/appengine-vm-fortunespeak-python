# Dockerfile extending the generic Python image with application files for a
# single application.
FROM google/appengine-python27

RUN apt-get update && apt-get install -y fortunes libespeak-dev
ADD requirements.txt /home/vmagent/app/
RUN pip install -r requirements.txt

ADD . /home/vmagent/app/
