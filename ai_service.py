import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_absence_message(teacher_name: str, course: str, note: str = "") -> str:
    """Generate a professional absence notification for students."""
    extra = f" Additional note: {note}" if note else ""
    prompt = (
        f"Write a short, professional Telegram notification (2-3 sentences) "
        f"informing students that {teacher_name} ({course}) will not be attending today's class.{extra} "
        f"Keep it polite and clear."
    )
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ {teacher_name} will not be present today for {course}. {note}"


async def generate_late_message(teacher_name: str, course: str, minutes: int = 0) -> str:
    """Generate a late-arrival notification."""
    time_str = f"approximately {minutes} minutes" if minutes else "a short while"
    prompt = (
        f"Write a brief, friendly Telegram message letting students know that "
        f"{teacher_name} ({course}) will be {time_str} late. Keep it under 2 sentences."
    )
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⏰ {teacher_name} ({course}) will be a few minutes late today."
