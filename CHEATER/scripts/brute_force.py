# Script needed about 1144 seconds to find key
# key was #\x9dc\xf6\x91w\xb4\xb4\xfe\x99`d\xf3\x85\xd5\xb2'
from Crypto.Cipher import AES
import time
import base64
import multiprocessing as mp


txt = base64.b64decode("/iealuDMPI7YVIVpmabxxNsXgBNycF67uLRTHC/R7PDX5sGnAsZJ3VjcVtjoouNnbt1zsvmUBW+WSPArZEIeIQ==")
txt = txt[:16]

mod = 0xA503F7833E4D480DE0AC0A4EE332D6EA39B32993B05BC35C10E2ADAA83DBC50287720AFBB5D621ED53B2583A8859DCE2710EBD266173FB9F58A2B9176B4DAC6992DE8FE8C12223C95F202C793C775E611B0E2B3EEE845CC7437CB58584D4874162B25AA511DDD57F6D7E966DEBA502A92AAAF941ED697373E79218999055B3AF
n = 68092650297014477609934827805824379289154348072603020680189820640479104313613222516735184755811404026665551443549194310400897074524560387037234082864526161829732398141477036611255832463573901678255009175477819822515853443579642434201463938434968181749992155554430451909101752976315316607530754147201264069226
peer_n = 29352994323089880583246046934418849353593803363498860556642555026496763840855791411506571309666024511333874079492801935349336787026785070708767540348291909205359635881068617515009487286161267818276992993293473994622906630204936995081649700968448034355998714040436944906584482940274271698280405787045156373979


RUN = 2 *  5939*  7243 # 1500000000

def run(start, end, q):
    t = time.time()
    for i in range(start, end):
        if not i % 10000000:
            print("At", i, " needed ", time.time() - t, " seconds for 10 mil.")
            t = time.time()
        key = pow(n, i, mod)
        key_b = key.to_bytes(128, "big")[-16:]
        cipher = AES.new(key_b, AES.MODE_ECB)
        cl = cipher.decrypt(txt)
        printable = True
        for c in cl:
            if not (32 <= c <= 125):
                printable = False
                break
        if printable:
            q.put((key_b, cl))
    q.put(b"end")

def main(cpus=4):

    space = RUN//cpus

    jobs = []
    q = mp.Queue()

    for i in range(cpus):
        j = mp.Process(target=run, args=(i*space, (i+1)*space, q))
        j.start()
        jobs.append(j)

    done_count = 0
    while True:
        k = q.get()
        if k == b"end":
            done_count += 1
        else:
            print("FOUND POSSIBLE KEY ", k[0], " : ", k[1])
        if done_count == cpus:
            break
        

    for j in jobs:
        j.terminate()
        j.join()


if __name__ == '__main__':
    start = time.time()
    main()
    needed = time.time() - start
    print("Needed ", needed)