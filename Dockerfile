#	Copyright 2015, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
FROM google/python

RUN apt-get update && apt-get install -y --no-install-recommends openssl ca-certificates libffi-dev

WORKDIR /app
RUN virtualenv /env
ADD requirements.txt /app/requirements.txt
RUN /env/bin/pip install -r /app/requirements.txt
ADD . /app

EXPOSE 8080
CMD []

# Using run.sh allows you to use one dockerfile for both the default and worker
# modules. The app.yaml/worker.yaml defines environment varables that run.sh
# uses to start the appropriate process.
ENTRYPOINT . /env/bin/activate; python main.py
