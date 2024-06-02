FROM python:3.9


COPY . /dev_sales

WORKDIR /dev_sales

# Install the dependencies
RUN pip install psycopg2
RUN pip install sqlalchemy
RUN pip install pandas
RUN pip install requests
RUN pip install matplotlib
COPY sales_data.csv sales_data.csv
COPY code_python.py code_python.py

CMD ["python", "code_python.py"]