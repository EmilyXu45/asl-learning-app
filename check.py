import os
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
missing = [l for l in alphabet if not os.path.exists(f"asl_images/{l}.png")]
print(f"You are missing these images: {missing}")