FROM python:3.7
WORKDIR /arima
ADD . /arima
COPY pip.conf /etc/pip.conf
RUN pip install -i https://pypi.mirrors.ustc.edu.cn/simple/  --no-cache-dir -r requirements.txt
EXPOSE 80
ENV NAME World
CMD ["python","arima_flask.py"]
