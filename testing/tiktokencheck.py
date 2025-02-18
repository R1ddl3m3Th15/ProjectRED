import tiktoken

# For a ChatCompletion with "gpt-3.5-turbo" or similar
enc = tiktoken.encoding_for_model("gpt-4")

system_msg = {"role": "system", "content": "You are a helpful assistant."}
user_msg = {"role": "user",
            "content": "Write a haiku about recursion in programming."}
assistant_msg = {"role": "assistant",
                 "content": "Code calls itself down,\nLayers of logic unfold,\nEndless paths converge."}


def count_chat_tokens(messages):
    tokens = 0
    for message in messages:
        tokens += 4  # Chat overhead per message
        tokens += len(enc.encode(message["content"]))
    tokens += 2  # Overall completion stop sequence
    return tokens


messages = [system_msg, user_msg, assistant_msg]
total_tokens = count_chat_tokens(messages)
print("Total tokens:", total_tokens)

encodings = tiktoken.list_encoding_names()
print(encodings)
