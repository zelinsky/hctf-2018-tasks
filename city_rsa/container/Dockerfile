FROM ubuntu:16.04

RUN \
  apt-get update && \
  DEBIAN_FRONTEND=noninteractive \
    apt-get -y install --no-install-recommends \
      tcpd \
      xinetd \
      python3 \
      libgmp-dev \
  && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/

RUN useradd backdoor --uid 1337

COPY xinetd/xinetd.conf /etc/xinetd.conf
COPY xinetd/ /etc/xinetd.d 

COPY bin/ /opt/
COPY verifier/ /opt/
RUN chmod o+x /opt/rsacrt

# -dontfork to stay in foreground
ENTRYPOINT [ "xinetd", "-dontfork" ]
