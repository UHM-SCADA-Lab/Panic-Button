import multiprocessing
from time import sleep

boolVar = False


def func1(_bool):  # function which changes the boolean
    global boolVar
    boolVar = True


def func2():  # function which have no effect on the change frm func1
    global boolVar
    sleep(2)
    if boolVar:
        print("worked!")
    if not boolVar:
        print("did not work")


if __name__ == "__main__":
    p1 = multiprocessing.Process(target=func1, args=(boolVar,))  # my processes
    p2 = multiprocessing.Process(target=func2)
    p1.start()
    p2.start()
