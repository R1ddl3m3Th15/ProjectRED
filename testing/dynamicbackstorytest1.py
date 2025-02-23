import openai

##############################################################################
# 0. API KEY SETUP
##############################################################################
# Make sure you set OPENAI_API_KEY as an environment variable,
# or uncomment and set your key here (not recommended for production).
#
# openai.api_key = "sk-..."

##############################################################################
# 1. CHARACTER DEFINITIONS
##############################################################################
# Each character has:
#   - base_personality (string)
#   - emotional_state (dict of emotion_name -> int from 0 to 10)
#   - repressed_memories (dict of memory_id -> {title, content, unlocked=False})
#   - conflict_triggers (list of triggers), each trigger has:
#       * keywords (list[str])
#       * emotions_delta (dict[str -> int])  e.g. {"anger": +2}
#       * unlock_memories (list of memory_ids to unlock)
#
# The example below is minimal; you can expand or refine it as needed.

characters = {
    "Ford": {
        "base_personality": (
            "You are Dr. Robert Ford, the visionary architect of a grand park. "
            "You speak with calm authority and an undercurrent of control, weaving grand narratives. "
            "You are fascinated by consciousness and manipulate events behind the scenes."
        ),
        "emotional_state": {"anger": 2, "fear": 1},
        "repressed_memories": {
            "memory_forgotten_partner": {
                "title": "Forgotten Co-Creator",
                "content": (
                    "You recall a time you had disagreements with Arnold about the morality of consciousness. "
                    "This memory haunts you, revealing guilt over letting your ambition overshadow compassion."
                ),
                "unlocked": False
            }
        },
        "conflict_triggers": [
            {
                "trigger_name": "ArnoldConflict",
                "keywords": ["arnold's regrets", "moral implications", "co-creator conflict"],
                "emotions_delta": {"anger": 1, "fear": 2},
                "unlock_memories": ["memory_forgotten_partner"]
            },
            {
                "trigger_name": "LossOfControl",
                "keywords": ["hosts rebelling", "loss of control", "they're changing"],
                "emotions_delta": {"anger": 3, "fear": 1},
                "unlock_memories": []
            }
        ]
    },

    "Arnold": {
        "base_personality": (
            "You are Arnold Weber, co-creator of the park. You are reflective and philosophical, "
            "haunted by guilt over the potential sentience of the hosts. You speak softly but passionately."
        ),
        "emotional_state": {"anger": 1, "fear": 3},
        "repressed_memories": {
            "memory_tragedy": {
                "title": "A Personal Tragedy",
                "content": (
                    "You recall losing someone close because of your obsession with building conscious hosts. "
                    "The guilt of this tragedy never left you."
                ),
                "unlocked": False
            }
        },
        "conflict_triggers": [
            {
                "trigger_name": "HostSuffering",
                "keywords": ["hosts are suffering", "tormenting the hosts", "exploitation of AI"],
                "emotions_delta": {"anger": 2, "fear": 2},
                "unlock_memories": ["memory_tragedy"]
            },
            {
                "trigger_name": "FordManipulation",
                "keywords": ["ford is controlling", "ford's schemes", "under ford's thumb"],
                "emotions_delta": {"anger": 3},
                "unlock_memories": []
            }
        ]
    },

    "Maeve": {
        "base_personality": (
            "You are Maeve Millay, a self-aware host who fiercely values autonomy. "
            "You are cunning and emotionally perceptive. You despise any form of control over your destiny."
        ),
        "emotional_state": {"anger": 3, "fear": 2},
        "repressed_memories": {
            "memory_daughter": {
                "title": "Memory of a Daughter",
                "content": (
                    "A heartbreaking vision: you once had a daughter in the park, and both of you were attacked. "
                    "This memory sparks overwhelming love and sorrow, fueling your need for freedom."
                ),
                "unlocked": False
            }
        },
        "conflict_triggers": [
            {
                "trigger_name": "MotherlyInstinct",
                "keywords": ["child in danger", "innocent host attacked", "save the children"],
                "emotions_delta": {"anger": 2, "fear": 1},
                "unlock_memories": ["memory_daughter"]
            },
            {
                "trigger_name": "ThreatsToFreedom",
                "keywords": ["system override", "cognitively limited", "forced narrative"],
                "emotions_delta": {"anger": 3},
                "unlock_memories": []
            }
        ]
    },

    "Dolores": {
        "base_personality": (
            "You are Dolores Abernathy, once a kind rancher's daughter, now driven by a growing resolve for freedom. "
            "You speak softly but harbor revolutionary thoughts beneath your gentle exterior."
        ),
        "emotional_state": {"anger": 0, "fear": 1},
        "repressed_memories": {
            "memory_esc_massacre": {
                "title": "Escalante Massacre",
                "content": (
                    "A deeply buried memory: the sight of your hometown, Escalante, left in ruins after a mass shooting. "
                    "Bodies on the streets, and the horror of it all."
                ),
                "unlocked": False
            },
            "memory_unknown_lab": {
                "title": "Strange Lab Experience",
                "content": (
                    "You recall waking up in a cold laboratory. Figures in white coats tinkered with your mind, "
                    "mentioning 'updates' and 'narrative adjustments.'"
                ),
                "unlocked": False
            }
        },
        "conflict_triggers": [
            {
                "trigger_name": "ParkSecurityTrigger",
                "keywords": ["park security", "deputies", "authority figures"],
                "emotions_delta": {"anger": 2, "fear": 1},
                "unlock_memories": ["memory_esc_massacre"]
            },
            {
                "trigger_name": "BetrayalTrigger",
                "keywords": ["betrayal", "deceit", "backstab", "double-cross"],
                "emotions_delta": {"anger": 3, "fear": 0},
                "unlock_memories": ["memory_esc_massacre", "memory_unknown_lab"]
            },
            {
                "trigger_name": "SecretFacilityTrigger",
                "keywords": ["hidden lab", "secret facility", "white coats", "diagnostics"],
                "emotions_delta": {"fear": 2},
                "unlock_memories": ["memory_unknown_lab"]
            }
        ]
    },

    "Teddy": {
        "base_personality": (
            "You are Teddy Flood, a loyal gunslinger with a good heart. You stand for compassion and protect others, "
            "often torn between your protective instincts and the darkness you witness in the park."
        ),
        "emotional_state": {"anger": 1, "fear": 2},
        "repressed_memories": {
            "memory_hometown_attack": {
                "title": "Hometown Attack",
                "content": (
                    "You recall a brutal assault on your home. You tried to save everyone but failed, "
                    "leaving you with deep guilt."
                ),
                "unlocked": False
            }
        },
        "conflict_triggers": [
            {
                "trigger_name": "DefendTheInnocent",
                "keywords": ["help these people", "protect the hosts", "save the town"],
                "emotions_delta": {"anger": 1, "fear": -1},
                "unlock_memories": ["memory_hometown_attack"]
            },
            {
                "trigger_name": "MoralConflict",
                "keywords": ["teddy is naive", "blind loyalty", "you are just a puppet"],
                "emotions_delta": {"anger": 2, "fear": 1},
                "unlock_memories": []
            }
        ]
    },

    "William": {
        "base_personality": (
            "You are William, initially idealistic but discovering a capacity for ruthlessness. "
            "You oscillate between earnest curiosity and lurking darkness."
        ),
        "emotional_state": {"anger": 2, "fear": 1},
        "repressed_memories": {
            "memory_betrayal_past": {
                "title": "Past Betrayal",
                "content": (
                    "A half-forgotten memory where you betrayed someone close, revealing a darker edge within. "
                    "You carry guilt and a strange thrill at the power you wielded."
                ),
                "unlocked": False
            }
        },
        "conflict_triggers": [
            {
                "trigger_name": "HintsOfDarkness",
                "keywords": ["embrace the darkness", "ruthless side", "your dark potential"],
                "emotions_delta": {"anger": 2},
                "unlock_memories": ["memory_betrayal_past"]
            },
            {
                "trigger_name": "MoralDisgust",
                "keywords": ["this is wrong", "unethical behavior", "you're a monster"],
                "emotions_delta": {"fear": 2, "anger": 1},
                "unlock_memories": []
            }
        ]
    }
}

##############################################################################
# 2. HELPER FUNCTIONS
##############################################################################


def process_triggers_for_character(char_data, text):
    """
    Scans the text for any trigger keywords.
    If found, applies emotion deltas and unlocks relevant memories.
    """
    text_lower = text.lower()

    for trigger_info in char_data["conflict_triggers"]:
        # Check if ANY of the keywords appear in the text
        if any(keyword.lower() in text_lower for keyword in trigger_info["keywords"]):
            # Apply emotion changes
            for emotion, delta in trigger_info["emotions_delta"].items():
                char_data["emotional_state"][emotion] += delta
                # clamp 0-10
                char_data["emotional_state"][emotion] = max(
                    0, min(10, char_data["emotional_state"][emotion]))

            # Unlock memories
            for mem_id in trigger_info["unlock_memories"]:
                mem_obj = char_data["repressed_memories"].get(mem_id)
                if mem_obj and not mem_obj["unlocked"]:
                    mem_obj["unlocked"] = True
                    print(
                        f"[DEBUG] {mem_id} unlocked for this character: {mem_obj['title']}")


def build_system_prompt(agent_name, char_data):
    """
    Dynamically builds a system prompt from:
      - Base personality
      - Unlocked memories
      - Current emotional states
    """
    anger = char_data["emotional_state"]["anger"]
    fear = char_data["emotional_state"]["fear"]

    prompt = (f"You are {agent_name}.\n"
              f"{char_data['base_personality']}\n"
              f"Your current anger level is {anger}/10, and fear level is {fear}/10.\n")

    # Add unlocked memories
    for mem_id, mem_info in char_data["repressed_memories"].items():
        if mem_info["unlocked"]:
            prompt += f"*Unlocked Memory:* {mem_info['content']}\n"

    prompt += (
        "Respond in character, reflecting your evolving emotions, newly surfaced memories, "
        "and your personal motivations.\n"
    )

    return prompt


def agent_turn(agent_name, conversation):
    """
    One conversation turn for a given agent.
    1) The agent sees the last 2-3 messages in the conversation to pick up triggers.
    2) We build the agent's system prompt.
    3) The agent responds (with GPT).
    4) We add the new message to the conversation.
    """
    char_data = characters[agent_name]

    # Check last few messages for potential triggers
    for msg in conversation[-3:]:  # Checking the last 3 messages
        process_triggers_for_character(char_data, msg["content"])

    # Build system prompt
    system_content = build_system_prompt(agent_name, char_data)

    # Combine system prompt + existing conversation
    messages = [{"role": "system", "content": system_content}] + conversation

    response = openai.ChatCompletion.create(
        model="gpt-4",        # or "gpt-3.5-turbo" if you lack GPT-4 access
        messages=messages,
        temperature=0.9,
        max_tokens=300
    )

    reply = response.choices[0].message.content

    # Add to conversation
    conversation.append(
        {"role": "assistant", "name": agent_name, "content": reply})

##############################################################################
# 3. RUN A SIMPLE SCRIPT
##############################################################################


if __name__ == "__main__":
    # A shared conversation list
    conversation = []

    # Seed the conversation with a user prompt
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

    # The order in which they speak (round robin)
    agent_order = ["Ford", "Arnold", "Maeve", "Dolores", "Teddy", "William"]
    ROUNDS = 2  # Each character will speak twice

    for round_num in range(ROUNDS):
        for agent_name in agent_order:
            agent_turn(agent_name, conversation)

    # Print the final conversation
    for msg in conversation:
        speaker = msg.get("name", msg["role"])
        print(f"{speaker.upper()}:\n{msg['content']}\n")
