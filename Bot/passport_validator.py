import idanalyzer as ia
from PIL import Image
from io import BytesIO
from telegram import Update, ForceReply
from telegram.ext import ContextTypes

async def validate_passport(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Validates a passport image uploaded by the user."""
    
    # Get the photo file ID from the update
    file_id = update.message.photo[-1].file_id
    
    # Download the photo using the bot's get_file method
    response = context.bot.get_file(file_id)
    
    # Check if the response is successful
    if response.status_code != 200:
        await update.message.reply_text("Failed to download the passport image.")
        return
    
    # Get the downloaded file content as bytes
    file_content = BytesIO(await response.download())
    
    try:
        # Load the image using PIL
        image = Image.open(file_content)
        
        # Analyze the image using id_analyzer_python
        analysis_result = ia.id_verify(image)
        
        # Check if the result is successful (i.e., the ID matches the document)
        if analysis_result["id"] == analysis_result["document"]:
            await update.message.reply_text("Passport image validated successfully!")
        else:
            await update.message.reply_text("Error validating passport image. Please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
        await update.message.reply_text("Failed to validate passport image. Please try again.")