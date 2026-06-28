import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")


def show(text):
    ids = enc.encode(text)

    print(f"tokens in {text}-> ")

    for id in ids :
        print(enc.decode([id]))

    print("\n")


show("strawberry")
show("pomogranate")
