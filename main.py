
# from fastapi import FastAPI

# app = FastAPI(
#     title="AI Customer Support Ticket Assistant",
#     description="API for managing customer support tickets",
#     version="1.0.0",
# )


# @app.get("/")
# def home():
#     return {
#         "message": "AI Customer Support Ticket Assistant API is running!"
#     }


# @app.get("/health")
# def health_check():
#     return {"status": "healthy"}


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from google.genai import types
from google import genai
from customer_support_agent.agent import runner, session_service
from customer_support_agent.classifier import classify_customer_issue
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()
# client = genai.Client()
from customer_support_agent.database import (
    create_database,
    save_ticket,
    get_all_tickets,
    update_ticket_status,
)

app = FastAPI(
    title="AI Customer Support Ticket Assistant",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_database()


class TicketRequest(BaseModel):
    customer_issue: str
    category: str


class StatusRequest(BaseModel):
    status: str


@app.get("/")
def home():
    return {"message": "AI Customer Support Ticket Assistant API is running!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# @app.post("/tickets")
# def create_ticket(request: TicketRequest):
#     if not request.customer_issue.strip():
#         raise HTTPException(status_code=400, detail="Issue cannot be empty")

#     return save_ticket(
#         request.customer_issue.strip(),
#         request.category,
#     )


@app.post("/tickets")
def create_ticket(request: TicketRequest):
    if not request.customer_issue.strip():
        raise HTTPException(
            status_code=400,
            detail="Issue cannot be empty",
        )

    issue = request.customer_issue.strip()
    category = classify_customer_issue(issue)

    return save_ticket(issue, category)


@app.get("/tickets")
def list_tickets():
    return [
        {
            "id": ticket[0],
            "customer_issue": ticket[1],
            "category": ticket[2],
            "status": ticket[3],
        }
        for ticket in get_all_tickets()
    ]


@app.patch("/tickets/{ticket_id}/status")
def change_ticket_status(ticket_id: int, request: StatusRequest):
    try:
        updated = update_ticket_status(ticket_id, request.status)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    if not updated:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return {"ticket_id": ticket_id, "status": request.status}

# @app.post("/ai-assist")
# async def ai_assist(request: TicketRequest):
#     issue = request.customer_issue.strip()

#     if not issue:
#         raise HTTPException(
#             status_code=400,
#             detail="Issue cannot be empty",
#         )

#     user_id = "support_user"
#     session_id = str(uuid4())

#     try:
#         await session_service.create_session(
#             app_name="customer_support",
#             user_id=user_id,
#             session_id=session_id,
#         )

#         content = types.Content(
#             role="user",
#             parts=[types.Part(text=issue)],
#         )

#         response_text = ""

#         async for event in runner.run_async(
#             user_id=user_id,
#             session_id=session_id,
#             new_message=content,
#         ):
#             if event.is_final_response() and event.content:
#                 response_text = "".join(
#                     part.text
#                     for part in event.content.parts or []
#                     if part.text
#                 )

#         if not response_text:
#             response_text = "AI did not return a response."

#         return {
#             "success": True,
#             "response": response_text,
#         }

# @app.post("/ai-assist")
# async def ai_assist(request: TicketRequest):
#     try:
#         category = classify_customer_issue(request.customer_issue)

#         result = client.interactions.create(
#             model="gemini-3.8-flash",
#             input=(
#                 "You are an AI customer support assistant. "
#                 f"Customer issue: {request.customer_issue}\n"
#                 f"Category: {category}\n"
#                 "Explain the issue category and suggest helpful next steps. "
#                 "Do not claim that a ticket was saved or that a refund "
#                 "or account change was completed."
#             ),
#         )

#         return {
#             "success": True,
#             "category": category,
#             "response": result.output_text,
#         }

#     except Exception as error:
#         print(f"AI agent error: {type(error).__name__}: {error}")
#         raise HTTPException(
#             status_code=503,
#             detail="AI service is temporarily unavailable. Please try again.",
#         )


@app.post("/ai-assist")
async def ai_assist(request: TicketRequest):
    try:
        client = genai.Client()

        category = classify_customer_issue(
            request.customer_issue
        )

        result = client.interactions.create(
            model="gemini-3.8-flash",
            input=(
                "You are an AI customer support assistant. "
                f"Customer issue: {request.customer_issue}\n"
                f"Category: {category}\n"
                "Explain the category and suggest helpful next steps. "
                "Do not claim a ticket was saved or that a refund "
                "or account change was completed."
            ),
        )

        return {
            "success": True,
            "category": category,
            "response": result.output_text,
        }

    except Exception as error:
        error_text = str(error)
        print(
            f"AI agent error: {type(error).__name__}: {error_text}"
        )

        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            return {
                "success": False,
                "error": "AI quota exceeded. Please try again later.",
                "fallback_available": True,
            }

        if "API key" in error_text or "api_key" in error_text:
            return {
                "success": False,
                "error": "Gemini API key is not configured.",
                "fallback_available": True,
            }

        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable.",
        )

    # except Exception as error:
    #     error_text = str(error)

    #     if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
    #         return {
    #             "success": False,
    #             "error": "AI quota exceeded. Please try again later.",
    #             "fallback_available": True,
    #         }

    #     raise HTTPException(
    #         status_code=503,
    #         detail="AI service is temporarily unavailable.",
    #     )

    
    except Exception as error:
        error_text = str(error)
        print(f"AI agent error: {type(error).__name__}: {error_text}")

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
        ):
            return {
                "success": False,
                "error": "AI quota exceeded. Please try again later.",
                "fallback_available": True,
            }

        if "API key" in error_text or "api_key" in error_text:
            return {
                "success": False,
                "error": "Gemini API key is not configured.",
                "fallback_available": True,
            }

        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable. Check the backend terminal.",
        )
