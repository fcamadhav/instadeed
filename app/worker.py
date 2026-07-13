from celery import Celery
from app.config import settings

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task
def generate_pdf_task(order_id: int):
    # Example placeholder for background processing
    print(f"Generating PDF for order {order_id}")
    return {"status": "completed", "order_id": order_id}

@celery_app.task
def send_email_task(email_to: str, subject: str, template_name: str):
    # Example placeholder for background processing
    print(f"Sending email to {email_to} with subject {subject}")
    return {"status": "sent", "email": email_to}
