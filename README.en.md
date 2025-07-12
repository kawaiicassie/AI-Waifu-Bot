[Tiếng Việt](./README.md)

# 🤖 Waifu Bot - A Versatile AI Assistant for Discord

Waifu Bot is not just a regular Discord bot, but a super cute AI "waifu" assistant, always ready to help her "master" with countless fun and useful features. The bot integrates multiple powerful AI models to deliver unique and creative experiences.

## ✨ Key Features

Here is a list of slash (/) commands that Waifu Bot supports:

-   🎨 `/imagine` - **Text-to-Image Generation**: Turn your ideas into artistic images with just one command.
-   💬 `/chat` - **Conversational Context**: Chat with Waifu, who will remember the conversation to interact naturally and charmingly.
-   🧠 `/solve` - **Reasoning & Problem Solving**: Pose challenging problems and let Waifu rack her brain to find the answer.
-   🖼️ `/describe` - **Image Description**: Upload an image and Waifu will tell you what's in it.
-   🧐 `/rate_art` - **Art Critique**: The discerning Waifu-sensei will provide in-depth reviews of your artwork.
-   🍳 `/cook` - **Home Chef**: Out of ideas for dinner? Provide the ingredients you have, and Chef Waifu will suggest a delicious recipe.
-   🌐 `/translate` - **Multilingual Translation**: Break down language barriers with ease.
-   🗣️ `/say` - **Text-to-Speech**: Let Waifu "read" the answers to you in various voices.
-   🗑️ `/forget` - **Clear Memory**: Start a completely new conversation with Waifu.

---

## ⚙️ Initial Setup: Creating a Bot on Discord

Before you can run the code, you need to create a "bot application" on Discord to get a `TOKEN`.

1.  **Create an Application**:
    -   Go to the [Discord Developer Portal](https://discord.com/developers/applications) and log in.
    -   Click the **"New Application"** button in the top right corner and give your bot a name.

2.  **Create a Bot and Get the Token**:
    -   In the left menu, select the **"Bot"** tab.
    -   Click **"Add Bot"** -> **"Yes, do it!"**.
    -   Below the bot's name, click **"Reset Token"** and copy this token. (**⚠️ DO NOT share this token with anyone!**)
    -   Scroll down and enable all 3 items under **Privileged Gateway Intents**:
        -   `PRESENCE INTENT`
        -   `SERVER MEMBERS INTENT`
        -   `MESSAGE CONTENT INTENT` (Crucial for the bot to read messages)

3.  **Invite the Bot to Your Server**:
    -   Go to the **"OAuth2"** tab -> **"URL Generator"**.
    -   Under **SCOPES**, check `bot` and `applications.commands`.
    -   A **BOT PERMISSIONS** box will appear below. Check the necessary permissions for the bot, for example:
        -   `Send Messages`
        -   `Read Message History`
        -   `Attach Files`
        -   `Use Slash Commands`
    -   Copy the generated URL from the **GENERATED URL** box below, paste it into your browser, and select the server you want to invite the bot to.

Now you have your `DISCORD_TOKEN` and the bot is in your server, ready to be launched!

---

## 🚀 Usage Guide
Get your Pollinations API Token at: [Pollinations.AI Auth](https://auth.pollinations.ai/)
API Documentation: [API Documentation](https://auth.pollinations.ai/)
Model list: [API Models](https://text.pollinations.ai/models)

You can deploy Waifu Bot in two ways:

### 1. Run Directly on Windows (Simple, for development purposes)

This method is suitable if you want to run the bot on your personal computer for testing or development.

1.  **Install Python**:
    -   Make sure you have [Python](https://www.python.org/downloads/) (version 3.10 or higher) installed.
    -   During installation, remember to check the `Add Python to PATH` box.

2.  **Clone the Repo and Install Dependencies**:
    ```bash
    # Clone the code to your machine
    git clone https://github.com/kawaiicassie/AI-Waifu-Bot.git
    cd AI-Waifu-Bot

    # Install necessary libraries
    pip install -r requirements.txt
    ```

3.  **Create a `.env` file**:
    -   Create a file named `.env` in the project's root directory.
    -   Add the following content to the file and replace it with your tokens:
        ```
        DISCORD_TOKEN="YOUR_DISCORD_BOT_TOKEN"
        POLLINATIONS_API_TOKEN="YOUR_API_TOKEN"
        ```

4.  **Run the Bot**:
    -   Open a Terminal (Command Prompt or PowerShell) and run the command:
        ```bash
        python bot.py
        ```
> **⚠️ Note**: The bot will only work while this terminal window is running and your computer is on.

### 2. Using Docker (Flexible, for deployment purposes)

If you want to host the bot on a VPS or a more stable environment, Docker is an excellent choice.

1.  **Clone the Repo**:
    ```bash
    git clone https://github.com/kawaiicassie/AI-Waifu-Bot.git
    cd AI-Waifu-Bot
    ```

2.  **Create a `.env` file**:
    -   Create a file named `.env` in the project's root directory.
    -   Add the following content to the file and replace it with your tokens:
        ```
        DISCORD_TOKEN="YOUR_DISCORD_BOT_TOKEN"
        POLLINATIONS_API_TOKEN="YOUR_API_TOKEN"
        ```

3.  **Build and Run the Docker Container**:
    -   Open a terminal and run the following commands:
        ```bash
        # Build the Docker image
        docker build -t image-name:latest .

        # Run the container in detached mode
        docker run -d --name container-name image-name:latest
        ```
    -   Your bot is now running inside the container!

---

## 💜 Final Words

If you find this project interesting and useful, don't hesitate to give it a ⭐ on GitHub! (´｡• ᵕ •｡`)♡

And if you have any cool ideas to improve our little Waifu, please **Fork** the repo and create a Pull Request. All contributions are valuable!

Thank you for visiting! (ﾉ´ヮ´)ﾉ*:･ﾟ✧
