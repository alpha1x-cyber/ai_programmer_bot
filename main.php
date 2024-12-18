<?php
// Import necessary libraries
use Monolog\Logger;
use Monolog\Handler\StreamHandler;
use Telegram\Bot\Api;

// Set up error logging
$logger = new Logger('name');
$logger->pushHandler(new StreamHandler('path/to/your.log', Logger::WARNING));

// Database for common errors and solutions by language
$error_solutions = [
    "python" => [
        "IndentationError" => "🔴 **IndentationError:**\n"
                              . "- Ensure that spaces or tabs are consistent in the code.\n"
                              . "- Try using a text editor that supports Python like VSCode or PyCharm.",
        "ModuleNotFoundError" => "🔴 **ModuleNotFoundError:**\n"
                                 . "- Ensure the library is installed using `pip install`.\n"
                                 . "- Check that the library name is spelled correctly.",
    ],
    "javascript" => [
        "SyntaxError" => "🔴 **SyntaxError:**\n"
                         . "- Check for properly closed brackets `{}` or `[]`.\n"
                         . "- Ensure to place a semicolon `;` if required.",
        "TypeError" => "🔴 **TypeError:**\n"
                       . "- Ensure that variables contain the correct values.\n"
                       . "- For example, a number cannot be called as a function.",
    ],
    "c++" => [
        "Segmentation fault" => "🔴 **Segmentation fault:**\n"
                                . "- Check pointers and ensure they point to valid memory locations.\n"
                                . "- Ensure memory is allocated using `new` or `malloc` if necessary.",
        "Compilation Error" => "🔴 **Compilation Error:**\n"
                               . "- Check for missing libraries or syntax errors."
    ]
];

// List of supported languages
$supported_languages = array_keys($error_solutions);

// /start command function
function start($update, $context) {
    $update->message->reply_text(
        "Welcome to the Programmer Bot! 👨‍💻\n"
        . "You can send code or describe the problem, and I will try to help you solve it 🚀.\n\n"
        . "💡 **Currently supported languages:**\n"
        . "- " . implode(", ", $supported_languages) . "\n\n"
        . "Just type the code or the problem, and I will start helping you!\n"
        . "Engineer Yassin's Programmer Bot"
    );
}

// /help command function
function help_command($update, $context) {
    $update->message->reply_text(
        "📚 **Usage Instructions:**\n\n"
        . "1. Send a message containing the code or programming error.\n"
        . "2. Mention the programming language in the message (e.g., Python, JavaScript, C++).\n"
        . "3. You will receive a clear and organized solution.\n\n"
        . "💡 The following languages are supported:\n"
        . "- " . implode(", ", $supported_languages) . "\n\n"
        . "❓ If you need further assistance, use the /start command."
    );
}

// Message handling function
function handle_message($update, $context) {
    $user_message = strtolower($update->message->text);

    // Determine the language from the message
    $language = null;
    foreach ($supported_languages as $lang) {
        if (strpos($user_message, $lang) !== false) {
            $language = $lang;
            break;
        }
    }

    if (!$language) {
        $update->message->reply_text(
            "❗ **I couldn't determine the programming language.**\n"
            . "Please mention the language in your message (e.g., Python, JavaScript, C++)."
        );
        return;
    }

    // Search for known errors in the text
    $solutions = [];
    foreach ($error_solutions[$language] as $error => $solution) {
        if (strpos($user_message, strtolower($error)) !== false) {
            $solutions[] = $solution;
        }
    }

    // Display solutions if found
    if ($solutions) {
        $response = "✅ **The following solutions were found:**\n\n" . implode("\n\n", $solutions);
    } else {
        $response = "❌ **I couldn't find a known error in your message for the language " . ucfirst($language) . ".**\n"
                  . "Please check the message or describe the problem more clearly.";
    }

    $update->message->reply_text($response, ['parse_mode' => 'Markdown']);
}

// Error logging function
function error($update, $context) {
    global $logger;
    $logger->warning('The following update caused an error: "%s"', $context->error);
}

// Main function to run the bot
function main() {
    // Place your bot token here
    $telegram_token = "7711679135:AAErrwekZ0Ym7i_PqWoW9ompV3eTvmAHsC8";

    // Create the Telegram API object
    $telegram = new Api($telegram_token);

    // Define commands for the bot
    $telegram->addCommand("start", "start");
    $telegram->addCommand("help", "help_command");
    $telegram->addMessageHandler("handle_message");

    // Start polling
    $telegram->startPolling();
}

if (php_sapi_name() == 'cli') {
    main();
}
?>