import streamlit as st
import random
from math import gcd

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="Ratio Quest",
    page_icon="🎮",
    layout="wide"
)

# -----------------------
# SESSION STATE
# -----------------------
if "score" not in st.session_state:
    st.session_state.score = 0

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "question_id" not in st.session_state:
    st.session_state.question_id = 0

if "question" not in st.session_state:
    st.session_state.question = None

if "answered" not in st.session_state:
    st.session_state.answered = False


# -----------------------
# QUESTION GENERATOR
# -----------------------
SCENARIOS = [
    ("🍕 Pizza Party", "pizza slices", "drinks"),
    ("🧪 Magic Potion", "dragon scales", "magic crystals"),
    ("⚽ Football Team", "boys", "girls"),
    ("🐶 Pet Shop", "dogs", "cats"),
    ("🚀 Space Mission", "rockets", "satellites"),
    ("🍎 Fruit Basket", "apples", "oranges"),
    ("🎮 Gaming Arena", "winners", "challengers"),
    ("🏴‍☠️ Pirate Crew", "pirates", "treasure chests")
]


def generate_question():
    while True:
        a = random.randint(1, 8)
        b = random.randint(1, 8)

        if gcd(a, b) == 1:
            break

    multiplier = random.randint(2, 10)

    equivalent_a = a * multiplier
    equivalent_b = b * multiplier

    title, item1, item2 = random.choice(SCENARIOS)

    return {
        "title": title,
        "item1": item1,
        "item2": item2,
        "base_a": a,
        "base_b": b,
        "answer_a": equivalent_a,
        "answer_b": equivalent_b,
        "multiplier": multiplier,
    }


def load_new_question():
    st.session_state.question = generate_question()
    st.session_state.question_id += 1
    st.session_state.answered = False


if st.session_state.question is None:
    load_new_question()

q = st.session_state.question

# -----------------------
# HEADER
# -----------------------
st.title("🎮 Ratio Quest")
st.subheader("Find Equivalent Ratios and Earn Points!")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("⭐ Score", st.session_state.score)

with col2:
    st.metric("🔥 Streak", st.session_state.streak)

with col3:
    level = st.session_state.score // 100 + 1
    st.metric("🏆 Level", level)

st.divider()

# -----------------------
# SCENARIO
# -----------------------
st.markdown(f"## {q['title']}")

st.info(
    f"""
Imagine you have a collection with:

**{q['base_a']} {q['item1']}** and
**{q['base_b']} {q['item2']}**

The ratio is:

# {q['base_a']} : {q['base_b']}

Can you create an equivalent ratio?
"""
)

# -----------------------
# INPUTS
# -----------------------
col1, col2 = st.columns(2)

with col1:
    user_a = st.number_input(
        f"Number of {q['item1']}",
        min_value=0,
        value=q["base_a"]
    )

with col2:
    user_b = st.number_input(
        f"Number of {q['item2']}",
        min_value=0,
        value=q["base_b"]
    )

# -----------------------
# CHECK ANSWER
# -----------------------
if st.button("✅ Check My Answer", use_container_width=True):

    if user_a == q["answer_a"] and user_b == q["answer_b"]:

        st.session_state.score += 10
        st.session_state.streak += 1

        st.success("🎉 Correct!")

        st.markdown(
            f"""
### Why is it correct?

Original ratio:

**{q['base_a']} : {q['base_b']}**

You multiplied BOTH numbers by **{q['multiplier']}**

**{q['base_a']} × {q['multiplier']} = {q['answer_a']}**

**{q['base_b']} × {q['multiplier']} = {q['answer_b']}**

So:

### {q['base_a']}:{q['base_b']} = {q['answer_a']}:{q['answer_b']}

Excellent work! 🚀
"""
        )

        st.balloons()

    else:

        st.session_state.streak = 0

        st.error("❌ Not quite right.")

        st.markdown(
            f"""
### Simple Explanation

To make an equivalent ratio, you must multiply BOTH parts by the SAME number.

Example:

**{q['base_a']} : {q['base_b']}**

Multiply both by **{q['multiplier']}**

→ **{q['answer_a']} : {q['answer_b']}**

Your answer changed the ratio, so it is not equivalent.
"""
        )

    st.session_state.answered = True

# -----------------------
# HINT
# -----------------------
with st.expander("💡 Need a Hint?"):
    st.write(
        "Equivalent ratios are made by multiplying BOTH numbers by the SAME value."
    )

# -----------------------
# NEXT QUESTION
# -----------------------
if st.session_state.answered:
    if st.button("🎲 Next Challenge", use_container_width=True):
        load_new_question()
        st.rerun()

# -----------------------
# PROGRESS BAR
# -----------------------
st.divider()

progress = min((st.session_state.score % 100) / 100, 1.0)

st.subheader("Level Progress")
st.progress(progress)

points_to_next = 100 - (st.session_state.score % 100)

st.write(f"🎯 {points_to_next} points until the next level.")

# -----------------------
# BADGES
# -----------------------
st.divider()

st.subheader("🏅 Badges")

badges = []

if st.session_state.score >= 20:
    badges.append("🥉 Ratio Rookie")

if st.session_state.score >= 50:
    badges.append("🥈 Ratio Explorer")

if st.session_state.score >= 100:
    badges.append("🥇 Ratio Master")

if st.session_state.streak >= 5:
    badges.append("🔥 Hot Streak")

if badges:
    for badge in badges:
        st.success(badge)
else:
    st.write("Earn points to unlock badges!")

# -----------------------
# INSTRUCTIONS
# -----------------------
with st.expander("📚 How to Play"):
    st.markdown(
        """
1. Read the ratio scenario.
2. Create an equivalent ratio.
3. Multiply BOTH numbers by the same value.
4. Check your answer.
5. Earn points and badges.

Example:

2 : 3

Multiply both by 4

8 : 12

These are equivalent ratios.
"""
    )
