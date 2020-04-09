FROM python:3

WORKDIR /usr/src/app

COPY ../../sensors .

RUN pip install --no-cache-dir -r sensors/heater_app/requirements.txt

CMD [ "python", "./sensors/heater_app/simulate_heater.py" ]