import subprocess
import time
import os
import sys

def run_backend():
    return subprocess.Popen([sys.executable, "backend.py"])

def run_frontend():
    os.chdir("chatbot-frontend")
    npm_path = os.path.join(os.path.dirname(sys.executable), 'npm.cmd' if sys.platform == "win32" else 'npm')
    return subprocess.Popen([npm_path, "start", "--", "--open"], shell=True)

if __name__ == "__main__":
    # Start the backend
    backend_process = run_backend()

    # Wait a bit for the server to start
    time.sleep(2)

    # Start the frontend
    # frontend_process = run_frontend()

    print("Application is running.")
    print("Backend is available at http://localhost:5000")
    # print("Frontend is available at http://localhost:4200")

    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Stop the backend and frontend when the user presses Ctrl+C
        backend_process.terminate()
        frontend_process.terminate()
        print("Application stopped")