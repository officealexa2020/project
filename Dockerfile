FROM python:latest

WORKDIR /project
ADD . /project
COPY project .
RUN pip3 install -r requirements.txt

RUN pip3 install jira

RUN pip3 install pandas

RUN pip3 install sk-learn


CMD ["python3","./jarvis_telegram.py"]
