FROM python:3
RUN pip3 install flask requests jsonify pyjson pyyaml
COPY getjson.py .
EXPOSE 8080
CMD [ "python3", "getjson.py" ]

