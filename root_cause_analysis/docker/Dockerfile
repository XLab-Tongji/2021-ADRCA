FROM python:3.7
WORKDIR /root_cause_analysis
ADD . /root_cause_analysis
COPY pip.conf /etc/pip.conf
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]