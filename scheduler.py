from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()

def start_scheduler(bot=None, groups=None):
    """
    Start the scheduler. Add reminder jobs here.
    Example: remind teachers to mark attendance at 8:00 AM daily.
    """
    # Uncomment and configure as needed:
    # scheduler.add_job(
    #     send_daily_reminder, "cron", hour=8, minute=0,
    #     args=[bot, groups]
    # )
    scheduler.start()
    logger.info("Scheduler started.")

async def send_daily_reminder(bot, groups):
    """Placeholder for a daily attendance reminder job."""
    from utils.notifications import notify_all_groups
    await notify_all_groups(bot, groups, "📢 Good morning! Teachers, please update your attendance status.")
