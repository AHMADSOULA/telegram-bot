import re
from telegram import Update, Document
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = "7996100508:AAEjmC2uNPHAYnvY4ECesvloesFYrH8sL9o"

# فحص البروكسي
def check_proxies(text):
    found = []
    lines = text.splitlines()

    for line in lines:
        line = line.strip()
        # بروكسي يبدأ بـ 34 او 35
        if re.match(r"^(34|35)\.", line):
            found.append(line)

    return found

# استقبال الملفات
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document: Document = update.message.document

    if not document.file_name.endswith(".txt"):
        await update.message.reply_text("ارسل ملف txt فقط")
        return

    file = await document.get_file()
    file_path = "file.txt"
    await file.download_to_drive(file_path)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    proxies = check_proxies(content)

    if proxies:
        result = "\n".join(proxies[:200])
        await update.message.reply_text(f"تم العثور على بروكسي:\n{result}")
    else:
        await update.message.reply_text("لا يوجد بروكسي يبدأ بـ 34 او 35")

# تشغيل
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

print("البوت شغال...")
app.run_polling()
