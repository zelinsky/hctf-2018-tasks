FROM ubuntu:16.04

RUN \
  apt-get update && \
  DEBIAN_FRONTEND=noninteractive \
    apt-get -y install --no-install-recommends \
      tcpd \
      xinetd \
      python3 \
  && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/

RUN useradd backdoor --uid 1337

COPY xinetd/ /etc/xinetd.d 
COPY app/ /opt/

# -dontfork to stay in foreground
ENTRYPOINT [ "xinetd", "-dontfork" ]
