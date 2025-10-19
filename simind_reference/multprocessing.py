import time 
import multiprocessing

def sleep_for_a_bit(seconds):
    print(f"Sleeping {seconds} second(s)")
    time.sleep(seconds)
    print("Done sleeping")


processes = []

for x in range(10):
    p = multiprocessing.Process(target=sleep_for_a_bit,args=[1])
    if __name__ == "__main__":
        p.start()
        processes.append(p)

for p in processes:
    p.join()


finish = time.perf_counter()
print("Finished running after seconds : ",finish)
