from nim import train, play


def main():
    ai = train(10000)
    play(ai)


if __name__ == "__main__":
    main()
