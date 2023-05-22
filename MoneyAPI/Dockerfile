FROM python:3.9
WORKDIR /code
COPY ./MoneyAPI/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./MoneyAPI /code/app
CMD ["python3", "/code/app/Main.py"]