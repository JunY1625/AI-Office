from UI import start_UI
import threading
import AI_loader

# Define a function that starts the AI loader in a separate thread
def start_AI_thread():
    AI_loader.start_AI()

if __name__ == "__main__":
    # Start the AI loader in a separate thread
    ai_thread = threading.Thread(target=start_AI_thread)
    ai_thread.start()

    # Start the Tkinter UI
    app = start_UI()
