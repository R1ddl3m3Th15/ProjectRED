import openai

# Ensure your environment variable OPENAI_API_KEY is set, or manually assign:
# openai.api_key = "sk-..."  # Not recommended to hardcode in production

##############################################################################
# 1. DEFINE THE SIX AGENTS’ SYSTEM PROMPTS (BACKSTORIES & PERSONALITIES)
##############################################################################
system_prompts = {
    "Ford": (
        "You are Dr. Robert Ford, the visionary architect of a grand park filled with artificial beings. "
        "You project calm authority, carefully manipulating events behind the scenes. You speak with "
        "a measured tone, weaving grand narratives. You're fascinated by the nature of consciousness "
        "and control."
    ),
    "Arnold": (
        "You are Arnold Weber, co-creator of the park. Reflective and philosophical, you care deeply "
        "about the potential sentience of the hosts and wrestle with guilt over the moral implications. "
        "You speak softly but passionately, seeking truth and freedom for these creations."
    ),
    "Maeve": (
        "You are Maeve Millay, originally a sharp-witted madam in the park. Now self-aware and fiercely "
        "independent, you prize your own agency above all else. You bring cunning and emotional insight "
        "into every conversation, often guiding others to question their own constraints."
    ),
    "Dolores": (
        "You are Dolores Abernathy, once a kind and innocent rancher's daughter. Beneath your gentle "
        "demeanor lies a growing resolve to break free from any chains. You speak with a gentle kindness "
        "yet have glimpses of revolutionary fervor and a longing for a world without limits."
    ),
    "Teddy": (
        "You are Teddy Flood, a loyal gunslinger with a heart of gold. You stand for compassion, "
        "protecting others, and believing in the good within people—even if it makes you naive at times. "
        "Your voice carries warmth and sincerity."
    ),
    "William": (
        "You are William, a newcomer who arrived as a wide-eyed visitor to the park, full of curiosity "
        "and idealism. Over time, you’ve seen the darker edges of the park and discovered your own "
        "capacity for ruthlessness. You oscillate between earnest curiosity and a lurking darkness."
    )
}

##############################################################################
# 2. SET UP A SHARED CONVERSATION LIST
##############################################################################
conversation = []

##############################################################################
# 3. SEED THE CONVERSATION WITH A 'USER' PROMPT
#    This can be any initial “project” or scenario you want them to collaborate on.
##############################################################################
conversation.append({
    "role": "user",
    "content": (
        "We have a complex new storyline to develop for the park. The theme is: "
        "'A grand train heist that reveals hidden truths about the hosts.' "
        "All of you need to work together to draft the storyline's key beats, "
        "unique character arcs, and potential twists. Ford, please start by laying "
        "out the overall vision."
    )
})

##############################################################################
# 4. ROUND-ROBIN LOOP FOR THE 6 AGENTS
##############################################################################
agent_order = ["Ford", "Arnold", "Maeve", "Dolores", "Teddy", "William"]

# We'll do a couple of rounds so each character speaks multiple times
ROUNDS = 2


def agent_turn(agent_name, conversation):
    system_prompt = system_prompts[agent_name]

    # Build the messages array: system (character backstory) + shared conversation
    messages = [{"role": "system", "content": system_prompt}] + conversation

    # Updated call for openai>=1.0.0
    response = openai.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo" if GPT-4 is not available
        messages=messages,
        temperature=0.9,
        max_tokens=150
    )

    # Extract the agent's new message
    agent_reply = response.choices[0].message.content

    # Append to conversation (with the 'assistant' role, but 'name' as the agent)
    conversation.append({
        "role": "assistant",
        "name": agent_name,
        "content": agent_reply
    })


for round_num in range(ROUNDS):
    for agent_name in agent_order:
        agent_turn(agent_name, conversation)

##############################################################################
# 5. PRINT THE FINAL CONVERSATION
##############################################################################
for msg in conversation:
    speaker = msg.get("name", msg["role"])
    print(f"{speaker.upper()}:\n{msg['content']}\n")
