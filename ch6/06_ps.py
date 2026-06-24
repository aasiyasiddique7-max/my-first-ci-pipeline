spam1 = "JOIN NOW"
spam2 = "BUY NOW"
spam3 = "SUBSCRIBE THIS"
spam4 = "CLICK THIS"

message = input("ENTER YOUR COMMENT")
if spam1 in message or spam2 in message or spam3 in message or spam4 in message:
    print("THIS IS SPAM")

else:
    print("IDGAF")