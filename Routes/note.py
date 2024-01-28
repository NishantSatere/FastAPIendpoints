from fastapi import APIRouter, HTTPException
from Models.note import Note
from bson import ObjectId 

from config.db import conn
from schemas.note import noteEntity, notesEntity

db = conn.notes

note = APIRouter()


@note.get("/", response_model=list)
def allNotes():
    try:
        # Fetch all notes from the 'notes' collection
        docs = db.notes.find({})
        # Convert the MongoDB documents to the desired format using notesEntity
        all_notes = notesEntity(docs)
        return all_notes
    
    except Exception as e:
        # Handle any exceptions that might occur during the database query
        print(f"Error retrieving notes: {e}")
        return []


@note.post("/", response_model=dict)
async def create_note(note_data: Note):
    try:
        # Insert a new note into the 'notes' collection
        result = db.notes.insert_one({
            "title": note_data.title,
            "desc": note_data.desc,
            "important": note_data.important
        })

        # Retrieve the created note from the 'notes' collection using its ObjectId
        created_note = db.notes.find_one({"_id": result.inserted_id})

        if not created_note:
            # If the created note is not found, raise an HTTPException
            raise HTTPException(status_code=500, detail="Failed to retrieve the created note")

        # Convert the created note to the desired format using noteEntity
        formatted_note = noteEntity(created_note)

        return formatted_note

    except Exception as e:
        # Handle any exceptions that might occur during the database operations
        print(f"Error creating note: {e}")
        raise HTTPException(status_code=500, detail="Failed to create note")
    

@note.get("/{note_id}", response_model=dict)
def get_note_by_id(note_id: str):
    try:
        # Convert the provided note_id string to a MongoDB ObjectId
        note_object_id = ObjectId(note_id)

        # Retrieve the note from the 'notes' collection using its ObjectId
        note_doc = db.notes.find_one({"_id": note_object_id})

        if not note_doc:
            # If the note is not found, raise an HTTPException with a 404 status code
            raise HTTPException(status_code=404, detail="Note not found")

        # Convert the retrieved note to the desired format using noteEntity
        formatted_note = noteEntity(note_doc)

        return formatted_note

    except Exception as e:
        # Handle any exceptions that might occur during the database operations
        print(f"Error retrieving note by ID: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve note by ID")
    


@note.delete("/{note_id}", response_model=dict)
def delete_note_by_id(note_id: str):
    try:
        # Convert the provided note_id string to a MongoDB ObjectId
        note_object_id = ObjectId(note_id)

        # Check if the note with the given ID exists
        existing_note = db.notes.find_one({"_id": note_object_id})
        if not existing_note:
            raise HTTPException(status_code=404, detail="Note not found")

        # Delete the note from the 'notes' collection using its ObjectId
        db.notes.delete_one({"_id": note_object_id})

        return {"message": "Note deleted successfully"}

    except Exception as e:
        # Handle any exceptions that might occur during the database operations
        print(f"Error deleting note by ID: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete note by ID")