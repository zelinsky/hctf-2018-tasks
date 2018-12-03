FROM alpine

WORKDIR /var/www/localhost/htdocs/
RUN apk add --update --no-cache lighttpd && rm -rf /var/cache/apk/*

ADD htdocs .
ADD config /etc/lighttpd/
RUN touch -t '200801021122' posts/* && touch -t '200805121337' posts/post_2008_05_12.txt && touch -t '200805121338' posts/post_2008_05_12.txt.sig.b64 && touch -t '200805131337' posts/post_2008_05_13.txt && touch -t '200805131339' posts/post_2008_05_13.txt && touch -t '200805141337' posts/post_2008_05_14.txt && touch -t '200805141337' posts/post_2008_05_14.txt && touch -t '200805131122' posts/post_2008_05_13.txt.sig.b64 && touch -t '200805141322' posts/post_2008_05_14.txt.sig.b64

EXPOSE 80

CMD ["lighttpd", "-D", "-f", "/etc/lighttpd/lighttpd.conf"]

