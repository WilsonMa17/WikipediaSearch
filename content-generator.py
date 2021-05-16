import tkinter as tk
import wikipedia
import sys
import csv
import zmq


def write_file(data):
    """Writes output to a csv file"""
    with open('output.csv', mode='w', newline='') as output_file:
        output_writer = csv.writer(output_file)
        output_writer.writerow(['input_keywords ', 'output_text'])
        output_writer.writerow(data)


def wikipedia_search(prim_key, second_key):
    """Takes a primary key and secondary key to search for a paragraph in Wikipedia"""
    # array is used to store the wikipedia page contents
    array = []
    search = wikipedia.search(prim_key)
    search = wikipedia.page(search[0], auto_suggest=False)

    # combines all page contents onto a single list element
    array = search.content
    array = [''.join(array)]
    # split single array into separate paragraph list elements
    split_content = [x.strip().split("\n") for x in array]
    final_array = []
    for paragraph in split_content:
        final_array = final_array + paragraph
    # checks if primary key and secondary key are in the paragraphs
    for content in final_array:
        if prim_key in content.split() and second_key in content.split():
            output_label = tk.Label(text="\nOutput Text: \n\n" + content, wraplength=300, justify="center")
            output_label.pack()
            write_file([prim_key, second_key, content.strip('\"')])
            break


def read_file(file):
    """Opens an input file and places all data into a list"""
    data = []
    with open(file) as file:
        # opens the file to read and places all read data into a list
        for line in file:
            data.append([v for v in line.split()])
    wikipedia_search(data[1][0].strip(';'), data[1][1])


def create_gui():
    """Builds a GUI window using TKinter"""
    window = tk.Tk()
    window.title("Content Generator")
    window.geometry("500x500")
    prim_label = tk.Label(text="Primary Keyword:",
                          fg="green")
    second_label = tk.Label(text="Secondary Keyword:",
                            fg="green")
    prim_entry = tk.Entry()
    second_entry = tk.Entry()
    prim_label.pack()
    prim_entry.pack()
    second_label.pack()
    second_entry.pack()
    prim_key = prim_entry.get()
    second_key = second_entry.get()

    def call():
        """function used by tk to call wikipedia search"""
        wikipedia_search(prim_entry.get(), second_entry.get())

    def destroy():
        """Exits the GUI"""
        window.destroy()

    # creates a button that calls the call()
    # function and runs the wikipedia search

    button = tk.Button(
        master=window,
        text="Generate",
        width=20,
        height=4,
        bg="black",
        fg="yellow",
        command=call
    )
    button.pack()
    clear_button = tk.Button(
        master=window,
        text='Clear',
    )
    clear_button.pack()
    destroy_button = tk.Button(
        master=window,
        text='Quit',
        command=destroy
    )
    destroy_button.pack()
    window.mainloop()


# Following 3 functions are helper functions for consume
# and feed microservice communication
def feed_data(prim_key, second_key):
    """Takes a primary key and secondary key to search for a paragraph in Wikipedia"""
    # array is used to store the wikipedia page contents
    array = []
    search = wikipedia.search(prim_key)
    search = wikipedia.page(search[0], auto_suggest=False)
    # combines all page contents onto a single list element
    array = search.content
    array = [''.join(array)]
    # split single array into separate paragraph list elements
    split_content = [x.strip().split("\n") for x in array]
    final_array = []
    for paragraph in split_content:
        final_array = final_array + paragraph
    # checks if primary key and secondary key are in the paragraphs
    for content in final:
        if prim_key in content.split() and second_key in content.split():
            output_label = tk.Label(text=content, wraplength=300, justify="center")
            output_label.pack()
            write_data([prim_key, second_key, content.strip('\"')])
            break
    # returns the corresponding paragraph if found
    return i


def feed(file_name):
    """Opens an input file and places all data into a list"""
    data = []
    with open(file_name) as file:
        # opens the file to read and places all read data into a list
        for line in file:
            data.append([(v) for v in line.split()])
    return feed_data(data[1][0].strip(';'), data[1][1])


def write_data(i):
    # Writes output to a csv file for microservice use
    with open('content_output.csv', mode='w', newline='') as output_file:
        output_writer = csv.writer(output_file)
        output_writer.writerow(['input_keywords ', 'output_text'])
        output_writer.writerow(i)


# runs gui when program is not passed any arguments
if len(sys.argv) == 1:
    create_gui()

# takes an input.csv if passed a filename argument
elif sys.argv[1] == "input.csv":
    read_file(sys.argv[1])

# FEED argv sends data to requesting program
elif sys.argv[1] == "feed":
    # Setup ZeroMQ library resources
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    # socket.bind sets up a server at port 5555 and actively listens for a connection
    socket.bind("tcp://*:5555")
    print("Sending data")
    while True:
        # listens for messages sent by other program
        message = socket.recv_string()
        print(message)
        data = feed(message)
        socket.send_string(str(data))

# CONSUME argv receives data from another program
elif sys.argv[1] == "consume":
    context = zmq.Context()
    # Socket connects to port 5555 server to begin communication
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    print("Requesting data")
    socket.send_string("pop_input.csv")
    message = socket.recv_string()
    print("received: " + message)

