import logging
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from flask import Flask

# إعداد نظام تسجيل الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# قاعدة بيانات للأخطاء الشائعة والحلول حسب اللغة
ERROR_SOLUTIONS = {
    "python": {
        "IndentationError": "🔴 **خطأ في التنسيق (IndentationError):**\n"
                            "- تأكد من أن المسافات (Spaces) أو التبويبات (Tabs) متناسقة في الكود.\n"
                            "- حاول استخدام محرر نصوص يدعم Python مثل VSCode أو PyCharm.",
        "ModuleNotFoundError": "🔴 **خطأ ModuleNotFoundError:**\n"
                               "- تأكد من تثبيت المكتبة باستخدام `pip install`.\n"
                               "- تحقق من كتابة اسم المكتبة بشكل صحيح.",
    },
    "javascript": {
        "SyntaxError": "🔴 **خطأ SyntaxError:**\n"
                       "- تحقق من وجود أقواس مغلقة بشكل صحيح `{}` أو `[]`.\n"
                       "- تأكد من وضع الفاصلة المنقوطة `;` إذا كان ذلك مطلوبًا.",
        "TypeError": "🔴 **خطأ TypeError:**\n"
                     "- تأكد من أن المتغيرات تحتوي على القيم الصحيحة.\n"
                     "- على سبيل المثال، لا يمكن استدعاء رقم كأنه دالة.",
    },
    "c++": {
        "Segmentation fault": "🔴 **خطأ Segmentation fault:**\n"
                              "- تحقق من المؤشرات (Pointers) وتأكد من أنها تشير إلى مواقع صحيحة في الذاكرة.\n"
                              "- تأكد من تخصيص الذاكرة باستخدام `new` أو `malloc` إذا لزم الأمر.",
        "Compilation Error": "🔴 **خطأ Compilation Error:**\n"
                             "- تحقق من وجود مكتبات مفقودة أو أخطاء في بناء الجملة (Syntax)."
    }
}

# قائمة اللغات المدعومة
SUPPORTED_LANGUAGES = ERROR_SOLUTIONS.keys()

# دالة /start للترحيب
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "مرحبًا بك في بوت المبرمج! 👨‍💻\n"
        "يمكنك إرسال الكود أو وصف المشكلة وسأحاول مساعدتك في حلها 🚀.\n\n"
        "💡 **اللغات المدعومة حاليًا:**\n"
        f"- {', '.join(SUPPORTED_LANGUAGES)}\n\n"
        "اكتب فقط الكود أو المشكلة وسأبدأ في مساعدتك!\n"
        "المبرمج بوت المهندس ياسين"
    )

# دالة /help لعرض المساعدة
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "📚 **تعليمات الاستخدام:**\n\n"
        "1. أرسل رسالة تحتوي على الكود أو الخطأ البرمجي.\n"
        "2. اذكر لغة البرمجة في الرسالة (على سبيل المثال: Python، JavaScript، C++).\n"
        "3. ستحصل على حل واضح ومنظم.\n\n"
        "💡 تدعم اللغات التالية:\n"
        f"- {', '.join(SUPPORTED_LANGUAGES)}\n\n"
        "❓ إذا كنت بحاجة إلى مساعدة إضافية، استخدم الأمر /start."
    )

# دالة لمعالجة الرسائل
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.lower()

    # تحديد اللغة من الرسالة
    language = None
    for lang in SUPPORTED_LANGUAGES:
        if lang in user_message:
            language = lang
            break

    if not language:
        update.message.reply_text(
            "❗ **لم أتمكن من تحديد لغة البرمجة.**\n"
            "يرجى ذكر اللغة في رسالتك (على سبيل المثال: Python، JavaScript، C++)."
        )
        return

    # البحث عن أخطاء معروفة في النص
    solutions = []
    for error, solution in ERROR_SOLUTIONS[language].items():
        if error.lower() in user_message:
            solutions.append(solution)

    # عرض الحلول إذا وجدناها
    if solutions:
        response = "✅ **تم العثور على الحلول التالية:**\n\n" + "\n\n".join(solutions)
    else:
        response = (
            f"❌ **لم أتمكن من العثور على خطأ معروف في رسالتك للغة {language.capitalize()}.**\n"
            "يرجى التحقق من الرسالة أو وصف المشكلة بشكل أوضح."
        )

    update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)

# دالة لتسجيل الأخطاء
def error(update: Update, context: CallbackContext) -> None:
    logger.warning('تسبب التحديث التالي بخطأ: "%s"', context.error)

# إعداد Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 تم تشغيل البوت بنجاح! يمكنك الآن استخدامه على Telegram."

# الدالة الرئيسية لتشغيل البوت
def main():
    # ضع رمز التوكن الخاص بالبوت هنا
    TELEGRAM_TOKEN = "7711679135:AAErrwekZ0Ym7i_PqWoW9ompV3eTvmAHsC8"

    # إنشاء الكائن Updater
    updater = Updater(TELEGRAM_TOKEN)

    # تعريف Dispatcher لإضافة الأوامر
    dispatcher = updater.dispatcher

    # إضافة الأوامر إلى البوت
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # تسجيل الأخطاء
    dispatcher.add_error_handler(error)

    # تشغيل Flask في خيط منفصل
    from threading import Thread
    Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 5000}).start()

    # بدء تشغيل البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()