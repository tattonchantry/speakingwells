from app.email import send_message_notification, send_welcome_email
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException, Depends
from app.email import send_message_notification
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from app.database import supabase
from app.models import *
from app.auth import hash_password, verify_password, create_access_token, decode_access_token
from app.qr import generate_qr_code
from fastapi.responses import StreamingResponse
import qrcode
import io

app = FastAPI(title="SpeakingWells API")

app.mount("/static", StaticFiles(directory="frontend"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_account(token: str = Depends(oauth2_scheme)):
    account_id = decode_access_token(token)
    if not account_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return account_id

@app.get("/")
def root():
    return FileResponse("frontend/index.html")

@app.post("/register")
def register(account: AccountCreate):
    existing = supabase.table("accounts").select("id").eq("email", account.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(account.password)
    result = supabase.table("accounts").insert({
        "email": account.email,
        "hashed_password": hashed,
        "shipping_address": account.shipping_address
    }).execute()
    send_welcome_email(account.email)
    return {"message": "Account created successfully"}

@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    result = supabase.table("accounts").select("*").eq("email", form.username).execute()
    if not result.data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    account = result.data[0]
    if not verify_password(form.password, account["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": account["id"]})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/cardholder")
def create_cardholder(cardholder: CardholderCreate, account_id: str = Depends(get_current_account)):
    existing = supabase.table("cardholders").select("id").eq("slug", cardholder.slug).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="That URL is already taken")
    result = supabase.table("cardholders").insert({
        "account_id": account_id,
        "name": cardholder.name,
        "color_scheme": cardholder.color_scheme,
        "slug": cardholder.slug,
        "photo_url": cardholder.photo_url,
        "card_message": cardholder.card_message
    }).execute()
    return result.data[0]

@app.get("/card/{slug}/data")
def get_card_data(slug: str):
    result = supabase.table("cardholders").select("name, slug, card_message, photo_url, color_scheme").eq("slug", slug).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Card not found")
    return result.data[0]

@app.get("/card/{slug}")
def get_card_page(slug: str):
    return FileResponse("frontend/card/index.html")

@app.post("/card/{slug}/message")
def send_message(slug: str, message: MessageCreate):
    card = supabase.table("cardholders").select("id, name, account_id").eq("slug", slug).execute()
    if not card.data:
        raise HTTPException(status_code=404, detail="Card not found")
    
    cardholder = card.data[0]
    
    # Save message to database
    supabase.table("messages").insert({
        "cardholder_id": cardholder["id"],
        "sender_name": message.sender_name,
        "sender_email": message.sender_email,
        "message_body": message.message_body
    }).execute()
    
    # Get family email
    account = supabase.table("accounts").select("email").eq("id", cardholder["account_id"]).execute()
    
    if account.data:
        send_message_notification(
            to_email=account.data[0]["email"],
            cardholder_name=cardholder["name"],
            sender_name=message.sender_name,
            sender_email=message.sender_email,
            message_body=message.message_body
        )
    
    return {"message": "Message sent successfully"}

@app.get("/card/{slug}/qr")
def get_qr_code(slug: str):
    result = supabase.table("cardholders").select("id").eq("slug", slug).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Card not found")
    qr_base64 = generate_qr_code(slug)
    return {"qr_code": qr_base64}

@app.get("/card/{slug}/qr.png")
def get_qr_image(slug: str):
    result = supabase.table("cardholders").select("id").eq("slug", slug).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Card not found")
    
    url = f"https://speakingwells.org/card/{slug}"
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    return StreamingResponse(buffer, media_type="image/png")

@app.get("/setup")
def setup():
    return FileResponse("frontend/setup.html")

@app.get("/slug-check/{slug}")
def check_slug(slug: str):
    result = supabase.table("cardholders").select("id").eq("slug", slug).execute()
    return {"available": len(result.data) == 0}

@app.get("/welcome")
def welcome():
    return FileResponse("frontend/welcome.html")
