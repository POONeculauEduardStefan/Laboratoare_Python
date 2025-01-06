import subprocess
import time


# Start the server with parameters 6 and 7 (board size)4
server_process = subprocess.Popen(['python', 'server.py','ai','10','10','player'])

# Wait a moment to ensure the server has started
time.sleep(1)

# Start two client processes
client1_process = subprocess.Popen(['python', 'client.py'])
# client2_process = subprocess.Popen(['python', 'client.py'])

# Wait for the clients to finish (or use `join()` to wait for all processes to end)
client1_process.wait()
# client2_process.wait()

# After the clients finish, stop the server
server_process.terminate()
server_process.wait()
