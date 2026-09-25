import os
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from jinja2 import Environment, PackageLoader, select_autoescape
from typing import Optional, List
from pydantic import EmailStr
from dotenv import load_dotenv

load_dotenv()

env= Environment(loader= PackageLoader("api"), autoescape= select_autoescape())

async def render_template(
    Template_name: str,
    Context: Optional[dict]
):
    template = env.get_template(Template_name)
    return template.render(Context)

async def send_mail(
    Subject: str,
    Recipients:  List[str], 
    Template_name: str,
    Context: Optional[dict]
):
    print(os.getenv("MAIL_FROM"))
    try:
        html = await render_template(Template_name= Template_name, Context= Context)
        config = ConnectionConfig(
            MAIL_USERNAME= os.getenv("EMAIL_USER"),
            MAIL_PASSWORD= os.getenv("EMAIL_PASSWORD"),
            MAIL_SERVER= os.getenv("MAIL_SERVER"), 
            MAIL_FROM= os.getenv("MAIL_FROM"),
            MAIL_STARTTLS= os.getenv("MAIL_STARTTLS"),
            MAIL_SSL_TLS= os.getenv("MAIL_SSL_TLS"),
            MAIL_PORT= os.getenv("MAIL_PORT")
        )

        message = MessageSchema(subject= Subject, recipients= Recipients, subtype= MessageType.html, body= html)
        fm = FastMail(config)
        await fm.send_message(message)  
    except  Exception as e:
        print(f"Error sending email{ e }")