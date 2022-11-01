FROM python:3.10.4

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt update && apt install -y wkhtmltopdf

COPY . .

EXPOSE 5000

ENV FLASK_ENV=development

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]