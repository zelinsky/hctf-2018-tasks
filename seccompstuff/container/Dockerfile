FROM ubuntu:16.04

RUN \
  apt-get update && \
  DEBIAN_FRONTEND=noninteractive \
    apt-get -y install --no-install-recommends \
      xinetd \
  && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/

RUN useradd chal --uid 1337

COPY xinetd/xinetd.conf /etc/xinetd.conf
COPY xinetd/ /etc/xinetd.d 

COPY bin/ /opt/
RUN chmod o+x /opt/seccomp

RUN echo "flag{e5eb5ea8b23cc29ed78166b67a2c70b00}" > /opt/flag.txt

# -dontfork to stay in foreground
ENTRYPOINT [ "xinetd", "-dontfork" ]
