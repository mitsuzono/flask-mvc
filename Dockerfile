FROM python:3.8

RUN mkdir /code
WORKDIR /code

# add files
ADD entrypoint.sh /code/entrypoint.sh
ADD src/ /code

# pip install
RUN pip install --upgrade pip --no-cache-dir
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 80
ENV PYTHONPATH "${PYTHONPATH}:/code/"
CMD ["/code/entrypoint.sh"]