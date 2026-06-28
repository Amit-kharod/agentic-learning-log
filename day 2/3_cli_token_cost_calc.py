import sys, tiktoken

PPMT = 0.15
PPT = PPMT / 1000000

def main():
    model = sys.argv[1]
    path = sys.argv[2]

    text = open(path).read()

    enc = tiktoken.encoding_for_model(model)
    ids = enc.encode(text)

    print(f"total words: {len(text.split())}")
    print(f"total tokens: {len(ids)}")
    print(f"total price: {(len(ids) * PPT):.6f}$")


if __name__ == "__main__":
    main()