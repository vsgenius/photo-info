import os
import threading
import redis
from flask import Flask, request, render_template

from db import Session, PhotoInfo

app = Flask(__name__)


def collect(directory, files, n, event_for_wait, event_for_set):
    with redis.Redis(host='redis', port=6379) as redis_client:
        for i in range(n):
            event_for_wait.wait()  # wait for event
            event_for_wait.clear()  # clean event for future
            f = open(directory + '/' + files[i], "rb").read()
            redis_client.set('files', f)
            event_for_set.set()  # set event for neighbor thread


def extract(n, event_for_wait, event_for_set):
    with redis.Redis(host='redis', port=6379) as redis_client:
        for i in range(n):
            event_for_wait.wait()
            event_for_wait.clear()
            with Session() as session:
                photo_info = PhotoInfo(size=len(redis_client.get('files')))
                session.add(photo_info)
                session.commit()
            event_for_set.set()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        directory = ''.join(request.form.getlist('dir'))
        files = os.listdir(os.curdir + '/' + directory)
        e1 = threading.Event()
        e2 = threading.Event()

        t1 = threading.Thread(target=collect, args=(directory, files, len(files), e1, e2))
        t2 = threading.Thread(target=extract, args=(len(files), e2, e1))

        t1.start()
        t2.start()

        e1.set()

        t1.join()
        t2.join()
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
