import string
import tkinter as tk
from tkinter import ttk, messagebox, font
from options import encryption_options

def temp():
    print('temp')


# class window
#   parent(s)
#       tk.Tk | tkinter Frame
#
#   description: creates the root window frame, and acts as the container / controller for the other frames of the
#       program.
class window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)  # set the root
        self.geometry('1600x900')

        # Font
        self.default_font = font.nametofont('TkDefaultFont')
        self.default_font.configure(family='Consolas', size=12)

        # Title
        self.title('_cipher')

        # create the main container
        container = tk.Frame(self)
        container.pack(side='top', fill='both')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in tuple([caesar, rail_fence, polybius_square]):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # Stack frames on top of each other.
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('Caesar')

    def show_frame(self, page_name):
        print('frame:', page_name)

        frame_name = page_name.replace(' ', '_').lower()
        frame = self.frames[frame_name]
        frame.tkraise()
        frame.option.set(page_name)


class caesar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Frames - Creation
        self.left_frame = tk.Frame(self, bg='orange', padx=25, pady=25)
        self.right_frame = tk.Frame(self, bg='cyan', padx=25, pady=25)

        # Frames - Layout
        self.left_frame.grid(row=0, column=0, sticky='nw')
        self.right_frame.grid(row=0, column=1, sticky='nw')

        # Widgets - Creation
        #  Left Frame
        #   Labels
        self.plain_text_label = tk.Label(self.left_frame, text='Plaintext')
        self.cipher_text_label = tk.Label(self.left_frame, text='Ciphertext')
        #   Text
        self.plain_text_widget = tk.Text(self.left_frame, width=75, height=15)
        self.cipher_text_widget = tk.Text(self.left_frame, width=75, height=15)
        #   Buttons
        self.encrypt_button = tk.Button(self.left_frame, command=lambda: self.encrypt(),
                                        text='Encrypt', anchor='w', width=10, height=1)
        self.decrypt_button = tk.Button(self.left_frame, command=lambda: self.encrypt(mode='d'),
                                        text='Decrypt', anchor='w', width=10, height=1)

        #  Right Frame
        self.method_label = tk.Label(self.right_frame, text='Encryption Method')
        self.key_label = tk.Label(self.right_frame, text='Key')
        self.alphabet_label = tk.Label(self.right_frame, text='Alphabet')

        self.option = tk.StringVar()
        self.option.set(encryption_options[0])

        self.encryption_method_menu = tk.OptionMenu(self.right_frame, self.option, *encryption_options,
                                                    command=lambda page_name: controller.show_frame(self.option.get()))
        self.encryption_method_menu.configure(width=20, anchor='w')

        self.key = tk.StringVar()
        self.key.set('3')
        self.key_entry = tk.Entry(self.right_frame, textvariable=self.key, width=10)

        self.alphabet_widget = tk.Text(self.right_frame, width=50, height=5)
        self.alphabet_widget.insert('1.0', string.ascii_lowercase)

        # Widgets - Layout
        #  Left Frame
        self.plain_text_label.grid(row=0, column=0, sticky='nw', pady=(0, 10))
        self.plain_text_widget.grid(row=1, column=0, sticky='nw')

        self.cipher_text_label.grid(row=2, column=0, sticky='nw', pady=(50, 10))
        self.cipher_text_widget.grid(row=3, column=0, sticky='nw')

        self.encrypt_button.grid(row=1, column=1, sticky='sw', padx=(10, 0))
        self.decrypt_button.grid(row=3, column=1, sticky='sw', padx=(10, 0))

        #  Right Frame
        self.method_label.grid(row=0, column=0, sticky='nw', pady=(0, 10))
        self.encryption_method_menu.grid(row=1, column=0, sticky='nw')

        self.key_label.grid(row=2, column=0, sticky='nw', pady=(25, 10))
        self.key_entry.grid(row=3, column=0, sticky='nw', pady=(0, 10))

        self.alphabet_label.grid(row=4, column=0, sticky='nw', pady=(25, 10))
        self.alphabet_widget.grid(row=5, column=0, sticky='nw')

        # Grid Configuration
        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)

    def encrypt(self, mode='e'):
        try:
            text, shifted_text = [], []
            alphabet = self.alphabet_widget.get('1.0', 'end-1c')
            alphabet_length = len(alphabet)
            key = int(self.key.get())

            if mode == 'e':
                text = self.plain_text_widget.get('1.0', 'end-1c').lower()
            else:
                text = self.cipher_text_widget.get('1.0', 'end-1c').lower()
                key = -key

            for char in text:
                if char in alphabet:
                    index = (alphabet.index(char) + key) % alphabet_length
                    shifted_text.append(alphabet[index])
                else:
                    shifted_text.append(char)

            shifted_text = ''.join(shifted_text)

            if mode == 'e':
                self.cipher_text_widget.delete('1.0', tk.END)
                self.cipher_text_widget.insert('1.0', shifted_text)
            else:
                self.plain_text_widget.delete('1.0', tk.END)
                self.plain_text_widget.insert('1.0', shifted_text)

        except ValueError as exception:
            if 'substring not found' in str(exception):
                messagebox.showwarning('Error', 'Internal Error\nSubstring Not Found')
            else:
                messagebox.showwarning('Error', 'Key is Invalid\nPlease set to an integer.')


class rail_fence(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Frames - Creation
        self.left_frame = tk.Frame(self, bg='orange', padx=25, pady=25)
        self.right_frame = tk.Frame(self, bg='cyan', padx=25, pady=25)

        # Frames - Layout
        self.left_frame.grid(row=0, column=0, sticky='nw')
        self.right_frame.grid(row=0, column=1, sticky='nw')

        # Widgets - Creation
        #  Left Frame
        #   Labels
        self.plain_text_label = tk.Label(self.left_frame, text='Plaintext')
        self.cipher_text_label = tk.Label(self.left_frame, text='Ciphertext')
        #   Text
        self.plain_text_widget = tk.Text(self.left_frame, width=75, height=15)
        self.cipher_text_widget = tk.Text(self.left_frame, width=75, height=15)
        #   Buttons
        self.encrypt_button = tk.Button(self.left_frame, command=self.encrypt, text='Encrypt', anchor='w',
                                        width=10, height=1)
        self.decrypt_button = tk.Button(self.left_frame, command=self.decrypt, text='Decrypt',
                                        anchor='w', width=10, height=1)

        #  Right Frame
        self.method_label = tk.Label(self.right_frame, text='Encryption Method')
        self.key_label = tk.Label(self.right_frame, text='Key')

        self.option = tk.StringVar()
        self.option.set(encryption_options[1])

        self.encryption_method_menu = tk.OptionMenu(self.right_frame, self.option, *encryption_options,
                                                    command=lambda page_name: controller.show_frame(self.option.get()))
        self.encryption_method_menu.configure(width=20, anchor='w')

        self.key = tk.StringVar()
        self.key.set('3')
        self.key_entry = tk.Entry(self.right_frame, textvariable=self.key, width=10)

        # Widgets - Layout
        #  Left Frame
        self.plain_text_label.grid(row=0, column=0, sticky='nw', pady=(0, 10))
        self.plain_text_widget.grid(row=1, column=0, sticky='nw')

        self.cipher_text_label.grid(row=2, column=0, sticky='nw', pady=(50, 10))
        self.cipher_text_widget.grid(row=3, column=0, sticky='nw')

        self.encrypt_button.grid(row=1, column=1, sticky='sw', padx=(10, 0))
        self.decrypt_button.grid(row=3, column=1, sticky='sw', padx=(10, 0))

        #  Right Frame
        self.method_label.grid(row=0, column=0, sticky='nw', pady=(0, 10))
        self.encryption_method_menu.grid(row=1, column=0, sticky='nw')

        self.key_label.grid(row=2, column=0, sticky='nw', pady=(25, 10))
        self.key_entry.grid(row=3, column=0, sticky='nw', pady=(0, 10))

        # Grid Configuration
        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)

    def encrypt(self):
        try:
            text, shifted_text = self.plain_text_widget.get('1.0', 'end-1c').lower(), ''
            key = int(self.key.get())
            rails = [['' for i in range(len(text))] for i in range(key)]

            x, y = 0, 0
            c_x, c_y = 1, 1

            for char in text:
                rails[x][y] = char

                x += c_x
                y += c_y

                if self.out_of_bounds(x, key):
                    c_x = -c_x
                    x += 2 * c_x

            for rail in rails:
                shifted_text += ''.join(rail)

            self.cipher_text_widget.delete('1.0', tk.END)
            self.cipher_text_widget.insert('1.0', shifted_text)

        except ValueError as exception:
            if 'substring not found' in str(exception):
                messagebox.showwarning('Error', 'Internal Error\nSubstring Not Found')
            else:
                messagebox.showwarning('Error', 'Key is Invalid\nPlease set to an integer.')

    def decrypt(self):
        try:
            text, shifted_text = self.cipher_text_widget.get('1.0', 'end-1c').lower(), ''
            text_length, key = len(text), int(self.key.get())
            rails = [['' for i in range(text_length)] for i in range(key)]
            current_rail, index = 0, 0

            for i in range(key):
                x, y = i, i
                c_x, c_y = 1, 1

                for j in range(text_length):
                    if x == current_rail:
                        rails[x][y] = text[index]
                        index += 1

                    x += c_x
                    y += c_y

                    if self.out_of_bounds(x, key):
                        c_x = -c_x
                        x += 2 * c_x

                current_rail += 1

            x, y = 0, 0
            c_x, c_y = 1, 1
            for i in range(text_length):
                shifted_text += rails[x][y]

                x += c_x
                y += c_y

                if self.out_of_bounds(x, key):
                    c_x = -c_x
                    x += 2 * c_x

            self.plain_text_widget.delete('1.0', tk.END)
            self.plain_text_widget.insert('1.0', shifted_text)

        except ValueError as exception:
            if 'substring not found' in str(exception):
                messagebox.showwarning('Error', 'Internal Error\nSubstring Not Found')
            else:
                messagebox.showwarning('Error', 'Key is Invalid\nPlease set to an integer.')

    @staticmethod
    def out_of_bounds(x, key):
        return x == -1 or x == key


class polybius_square(tk.Frame):
    starting_alphabet = string.ascii_lowercase.replace('j', '')
    starting_rows = starting_columns = '12345'
    starting_seperator = '-'

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Frames - Creation
        self.left_frame = tk.Frame(self, bg='orange', padx=25, pady=25)
        self.right_frame = tk.Frame(self, bg='cyan', padx=25, pady=25)
        self.keys_frame = tk.Frame(self.right_frame, bg='blue')

        # Frames - Layout
        self.left_frame.grid(row=0, column=0, sticky='nw')
        self.right_frame.grid(row=0, column=1, sticky='nw')
        self.keys_frame.grid(row=2, column=0, rowspan=2, columnspan=3, sticky='nw')

        # Widgets - Creation
        self.set_polybius_square(self.starting_rows, self.starting_columns, self.starting_alphabet)

        # Left Frame
        # Labels
        self.plain_text_label = tk.Label(self.left_frame, text='Plaintext')
        self.cipher_text_label = tk.Label(self.left_frame, text='Ciphertext')
        # Text
        self.plain_text_widget = tk.Text(self.left_frame, width=75, height=15)
        self.cipher_text_widget = tk.Text(self.left_frame, width=75, height=15)
        # Buttons
        self.encrypt_button = tk.Button(self.left_frame, command=self.encrypt, text='Encrypt',
                                        anchor='w',width=10, height=1)
        self.decrypt_button = tk.Button(self.left_frame, command=temp, text='Decrypt',
                                        anchor='w', width=10, height=1)

        #  Right Frame
        self.method_label = tk.Label(self.right_frame, text='Encryption Method')
        self.alphabet_label = tk.Label(self.right_frame, text='Alphabet')

        self.option = tk.StringVar()
        self.option.set(encryption_options[1])
        self.encryption_method_menu = tk.OptionMenu(self.right_frame, self.option, *encryption_options,
                                                    command=lambda page_name: controller.show_frame(self.option.get()))
        self.encryption_method_menu.configure(width=20, anchor='w')

        self.alphabet_widget = tk.Text(self.right_frame, width=50, height=5)
        self.alphabet_widget.insert('1.0', self.starting_alphabet)

        # Keys Frame
        self.rows_label = tk.Label(self.keys_frame, text='Rows')
        self.columns_label = tk.Label(self.keys_frame, text='Columns')
        self.seperator_label = tk.Label(self.keys_frame, text='Seperator')

        self.rows = tk.StringVar()
        self.rows.set(self.starting_rows)
        self.rows_entry = tk.Entry(self.keys_frame, textvariable=self.rows, width=10)

        self.columns = tk.StringVar()
        self.columns.set(self.starting_columns)
        self.columns_entry = tk.Entry(self.keys_frame, textvariable=self.columns, width=10)

        self.seperator = tk.StringVar()
        self.seperator.set(self.starting_seperator)
        self.seperator_entry = tk.Entry(self.keys_frame, textvariable=self.seperator, width=10)

        # Row Labels

        # Widgets - Layout
        #  Left Frame
        self.plain_text_label.grid(row=0, column=0, sticky='nw', pady=(0, 10))
        self.plain_text_widget.grid(row=1, column=0, sticky='nw')

        self.cipher_text_label.grid(row=2, column=0, sticky='nw', pady=(50, 10))
        self.cipher_text_widget.grid(row=3, column=0, sticky='nw')

        self.encrypt_button.grid(row=1, column=1, sticky='sw', padx=(10, 0))
        self.decrypt_button.grid(row=3, column=1, sticky='sw', padx=(10, 0))

        #  Right Frame
        self.method_label.grid(row=0, column=0, sticky='nw', pady=(0, 10))
        self.encryption_method_menu.grid(row=1, column=0, sticky='nw')

        #   Keys Frame - Start
        self.rows_label.grid(row=0, column=0, sticky='nw', padx=(0, 25), pady=(25, 10))
        self.rows_entry.grid(row=1, column=0, sticky='nw', padx=(0, 25), pady=(0, 10))

        self.columns_label.grid(row=0, column=1, sticky='nw', padx=(0, 25), pady=(25, 10))
        self.columns_entry.grid(row=1, column=1, sticky='nw', padx=(0, 25), pady=(0, 10))

        self.seperator_label.grid(row=0, column=2, sticky='nw', pady=(25, 10))
        self.seperator_entry.grid(row=1, column=2, sticky='nw', pady=(0, 10))
        #   Keys Frame - End

        self.alphabet_label.grid(row=4, column=0, sticky='nw', pady=(25, 10))
        self.alphabet_widget.grid(row=5, column=0, sticky='nw')

        # Grid Configuration
        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)

    def set_polybius_square(self, rows, columns, alphabet):
        try:
            num_rows, num_columns = len(rows), len(columns)
            self.p_square_matrix = {}
            self.p_square = [[] for i in range(num_rows)]
            alphabet_length, index = len(alphabet), 0

            for i in range(num_rows):
                for j in range(num_columns):
                    if index < alphabet_length:
                        self.p_square_matrix[alphabet[index]] = rows[i] + columns[j]
                        self.p_square[i].append(alphabet[index])
                        index += 1
                    else:
                        self.p_square[i].append('')

                print(f'i = {i} | {self.p_square[i]}')

            print('\np_square_matrix')
            for key in self.p_square_matrix.keys():
                print(f'{key} | {self.p_square_matrix[key]}')

        except ValueError as exception:
            if 'substring not found' in str(exception):
                messagebox.showwarning('Error', 'Internal Error\nSubstring Not Found')
            else:
                messagebox.showwarning('Error', 'Key is Invalid\nPlease set to an integer.')

    def encrypt(self):
        try:
            self.set_polybius_square(self.rows.get(), self.columns.get(),
                                     self.alphabet_widget.get('1.0', 'end-1c').lower())
            plain_text, cipher_text = self.plain_text_widget.get('1.0', 'end-1c').lower(), ''
            seperator = self.seperator.get()
            keys = self.p_square_matrix.keys()

            for char in plain_text:
                if char in keys:
                    cipher_text += self.p_square_matrix[char] + seperator

            cipher_text = cipher_text.strip(seperator)

            self.cipher_text_widget.delete('1.0', tk.END)
            self.cipher_text_widget.insert('1.0', cipher_text)


        except ValueError as exception:
            if 'substring not found' in str(exception):
                messagebox.showwarning('Error', 'Internal Error\nSubstring Not Found')
            else:
                messagebox.showwarning('Error', 'Key is Invalid\nPlease set to an integer.')