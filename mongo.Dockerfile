FROM mongo

ARG USER_ID

RUN adduser --shell /bin/bash --disabled-password --gecos "" --uid $USER_ID mongo
RUN chown -R mongo /data/db
USER mongo
