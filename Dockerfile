FROM python
WORKDIR /usr/src/conf_bot/
COPY . ./
RUN pip3 install -r requirements.txt
CMD [ "python3", "bot.py" ]