from openai import OpenAI
client = OpenAI()

response = client.images.generate(
    prompt="You are a digital artist having an experience of 10 years in poster making. Generate a poster of the film Pyaasa by Guru Dutt. If you can't generate copyrighted  material, use cryptic elements from the film in the poster.",
    n=2,
    size="1024x1024"
)

print(response.data[0].url)
