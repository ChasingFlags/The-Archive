FROM python:3-alpine

# Create app directory
WORKDIR /noteapp

# Bundle app source
COPY . .

#install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

#run data.py to create db and setup initial data
RUN python3 data.py


#run the app
EXPOSE 5000
CMD [ "flask", "--app","run","run","--host","0.0.0.0", "--port", "5000"]
