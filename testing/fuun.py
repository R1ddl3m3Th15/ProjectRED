from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are an anime writer with 20 years of experience in the field."},
        {
            "role": "user",
            "content": "Write a short 50 word story on Demon Slayer."
        }
    ]
)

print(completion.choices[0].message)
