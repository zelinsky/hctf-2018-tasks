FROM ubuntu:16.04

RUN \
  apt-get update && \
  DEBIAN_FRONTEND=noninteractive \
    apt-get -y install --no-install-recommends \
      xinetd \
  && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/

RUN useradd slottiermachine --uid 1337

COPY xinetd/xinetd.conf /etc/xinetd.conf
COPY xinetd/slottiermachine_svc /etc/xinetd.d/

RUN mkdir -p /var/jail
COPY rootfs/ /var/jail/

RUN for i in $(/var/jail/bin/busybox-x86_64 --list);do ln -s /bin/busybox-x86_64 /var/jail/bin/$i;done

RUN chmod o+x /var/jail/opt/slottiermachine /var/jail/bin/busybox-x86_64

ENTRYPOINT [ "xinetd", "-dontfork" ]
