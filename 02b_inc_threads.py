from concurrent.futures import ThreadPoolExecutor

val = 0


def inc():
    global val

    if val < 10:
        print("increasing")
        val += 1


def main():
    with ThreadPoolExecutor(max_workers=100) as executor:
        [executor.submit(inc) for _ in range(100)]

    print(val)


if __name__ == "__main__":
    main()
