from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from database import supabase
from auth import get_current_user


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