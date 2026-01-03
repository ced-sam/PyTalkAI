# Mistral Chat Client

A simple GUI chat client for interacting with the [Mistral AI API](https://mistral.ai/). This application allows you to send messages to the Mistral API and display the responses in a user-friendly interface built with `customtkinter`.

## Features
- Send messages to the Mistral API and display responses in real-time.
- Navigate through message history using the **Up** and **Down** arrow keys.
- Copy messages to the clipboard with a right-click or **Ctrl+C**.
- Dark mode interface for a modern look.

## Requirements
- Python 3.8 or higher
- `customtkinter` (for the GUI)
- `requests` (for API calls)
- A valid [Mistral API key](https://mistral.ai/)

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/mistral-chat-client.git
   cd mistral-chat-client
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your Mistral API key:
   ```env
   OPENAI_API_KEY=your_mistral_api_key_here
   ```

4. Run the application:
   ```bash
   python chat.py
   ```

## Usage
- Type your message in the input box and press **Enter** or click the **Send** button to submit.
- Use the **Up** and **Down** arrow keys to navigate through your message history.
- Click the **Copy All** button to copy the entire conversation to your clipboard.
- Click the **Clear** button to erase the conversation.

## License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Disclaimer
This project is not affiliated with or endorsed by Mistral AI. Use of the Mistral API is subject to their [terms and conditions](https://mistral.ai/terms/).