# Company App

## About Project
...

## How to run

### Docker
```
docker-compose up --build
docker container ls
docker exec (name of web service) alembic upgrade head  
```


### Another way -

* Create .env file in root directory
```
PORT=your
HOST=your
DEBUG=Your
```

### Windows
```
1 - virtualenv myenv
2 - myenv\Scripts\activate
3 -  pip3 install -r requirements.txt
4 - uvicorn app.server:app
```


### Linux
```
1 - python3 -m venv venv 
2 - source venv/bin/activate
3 -  pip3 install -r requirements.txt
4 - uvicorn app.server:app
```
