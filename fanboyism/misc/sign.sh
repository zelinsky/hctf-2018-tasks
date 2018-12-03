# run as:
# bash ../../../misc/sign.sh in posts folder 
for i in $(ls *.txt); do
openssl dgst -sha256 -sign ../../../misc/38b2cc8ca9cff6705d8556bbe7682e82-9707 ${i}| openssl base64 -in /dev/stdin -out ${i}.sig.b64
done
