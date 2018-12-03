FROM ubuntu:16.04

RUN \
  apt-get update && \
  DEBIAN_FRONTEND=noninteractive \
    apt-get -y install --no-install-recommends \
      tcpd \
      xinetd \
  && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/

RUN useradd backdoor --uid 1337

COPY xinetd/xinetd.conf /etc/xinetd.conf
COPY xinetd/backdoor_svc /etc/xinetd.d 

RUN mkdir -p /var/jail/bin
COPY jail/busybox /var/jail/bin
RUN ln -s /bin/busybox /var/jail/bin/sh && ln -s /bin/busybox /var/jail/bin/ls &&  ln -s /bin/busybox /var/jail/bin/cat
RUN chmod o+x /var/jail/bin/busybox

RUN echo "flag{Pr3tty_Obvi0us_B4ckd00r}" > /var/jail/flag.txt

# -dontfork to stay in foreground
ENTRYPOINT [ "xinetd", "-dontfork" ]
