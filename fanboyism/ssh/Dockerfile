FROM ubuntu:16.04

RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo "PasswordAuthentication no" >> /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
RUN useradd -m jan0sh && mkdir /home/jan0sh/.ssh/ && echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAvowhzrTHPoF+oBRkS187VWHPG86+A2zBD9J+jmLT0ThBX0o71XtjEkCOtMJWTyqCScGKzlHTicwe80iTxtO6hof9kXAz6P2P/S3V+xWbOeaxAmD2LWCK7fcmaR6LpInkBqNUWZdShgvswS6n/M1CurK8BywAHLsQHDvyWnSroOo428qHDBTCzMtkiXH6ng8KQKIrQT20KrK2FgOJe24BwNMo2i+tcykCnGLDseZOTX7JmckMXTMXILv2pDfgxFAvCVNMo7q5hnnTmqyRZexcqapDqO/eBs01jNAj6T4wuWv4HqpG3PzcbpUf6JR1z5hmR/+7KR39ynxGLI3fnbtdhQ== jan0sh@debian" >  /home/jan0sh/.ssh/authorized_keys

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile
RUN echo "flag{I_guess_random_numbers_are_important_lol}" > /home/jan0sh/flag.txt
RUN chown root: /home/jan0sh -R

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
