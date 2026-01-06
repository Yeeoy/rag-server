import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel


from database import supabase
from auth import get_current_user

load_dotenv()

llm = ChatOpenAI(model=os.getenv("DEEPSEEK_MODEL"), temperature=0)

router = APIRouter(tags=["chats"])

class ChatCreate(BaseModel):
    title: str
    project_id: str
    
@router.post("/api/chats")
async def create_chat(
    chat: ChatCreate,
    clerk_id: str = Depends(get_current_user)
):
    try:
        result = supabase.table("chats").insert({
            "title": chat.title,
            "project_id": chat.project_id,
            "clerk_id": clerk_id
        }).execute()

        return {
            "message":"Project files retrieved successfully",
            "data": result.data[0]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create project chat: {str(e)}") 
    
@router.delete("/api/chats/{chat_id}")
async def delete_chat(
    chat_id: str,
    clerk_id: str = Depends(get_current_user)
):
    try:
        result = supabase.table("chats").delete().eq("id", chat_id).eq("clerk_id", clerk_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail=f"Failed to delete project chat: {str(e)}") 

        return {
            "message":"Project chat deleted successfully",
            "data": result.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete project chat: {str(e)}") 
    
@router.get("/api/chats/{chat_id}")
async def get_chat(
    chat_id: str,
    clerk_id: str = Depends(get_current_user)
):
    try:
        result = supabase.table('chats').select("*").eq("id",chat_id).eq("clerk_id", clerk_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail=f"Chat not found or access denied")
        
        chat = result.data[0]
        
        messages_result = supabase.table("messages").select("*").eq("chat_id",chat_id).order('created_at', desc=False).execute()
        
        chat['messages'] = messages_result.data or []
        
        return {
            "message": "Chat retrieved successfully",
            "data": chat
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get project chat: {str(e)}") 

class SendMessageRequest(BaseModel):
    content: str

@router.post("/api/projects/{project_id}/chats/{chat_id}/messages")
async def send_message(
    chat_id: str,
    request: SendMessageRequest,
    clerk_id: str = Depends(get_current_user)
):
    try:
        message = request.content
        
        print(f"ℹ️ New Message: {message[:50]}...")
        
        print("Saving user message...")
        user_message_result = supabase.table('messages').insert({
            "chat_id": chat_id,
            "content": message,
            "role": "user",
            "clerk_id": clerk_id
        }).execute()
        
        user_message = user_message_result.data[0]
        print(f"✅ User message saved: {user_message['id']}")
        
        print("Calling LLM")
        messages = [
            SystemMessage(content="你是一个乐于助人的 AI 助手，请使用清晰、简洁、准确的方式回答用户的问题"),
            HumanMessage(content=message)
        ]
        
        response = llm.invoke(messages)
        ai_response = response.content
        
        print(f"✅ LLM response received: {len(ai_response)} chars")
        
        print("Saving AI message...")
        ai_message_result = supabase.table("messages").insert({
            "chat_id": chat_id,
            "content": ai_response,
            "role": "assistant",
            "clerk_id": clerk_id,
            "citations": []
        }).execute()
        
        ai_message = ai_message_result.data[0]
        print(f"✅ AI Message saved: {ai_message['id']}")
        
        return {
            "message": "Messages sent successfully",
            "data":{
                "userMessage": user_message,
                "aiMessage": ai_message
            }
        }
        
    except Exception as e:
        print(f"❌ Error in send_message: {str(e)}")
        raise HTTPException(status_code=500, details= str(e))