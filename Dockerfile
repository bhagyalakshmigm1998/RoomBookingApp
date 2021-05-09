FROM python:3 
WORKDIR /usr/src/booking
COPY requirements.txt . 
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . . 
ENTRYPOINT [ "python" ]
CMD [ "booking.py" ]
