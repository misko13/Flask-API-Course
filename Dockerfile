FROM python:3.12.1
# EXPOSE 5000   
EXPOSE 80   
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
#CMD ["flask", "run", "--host", "0.0.0.0"]
CMD [ "calc", "--bind" , "0.0.0.0:80", "app:create_app()"]