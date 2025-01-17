from tkinter import Tk, Listbox, Button, Label, Toplevel, END, Entry
from tkinter.constants import SINGLE

from sqlalchemy_database import engine, Product
from sqlalchemy.orm import sessionmaker


class Window:
    def __init__(self):
        self.master = Tk()
        self.master.geometry('500x350')

    def open_new_window(self):
        top_level_master = Toplevel(self.master)
        top_level_master.grab_set()


class MainWindow(Window):
    def __init__(self):
        super().__init__()

        self.listbox = Listbox(self.master, selectmode=SINGLE)
        self.name_label = Label(self.master, text='Product Name ')
        self.how_much_left_label = Label(self.master, text='How much left, g ')
        self.cost_label = Label(self.master, text='Cost, euro ')
        self.error_label = Label(self.master, text='')

        self.name_entry = Entry(self.master)
        self.how_much_left_entry = Entry(self.master)
        self.cost_entry = Entry(self.master)

        self.submit_button = Button(self.master, text='Submit', command=self.submit_to_database)
        self.delete_selected_button = Button(self.master, text='Delete Selected', command=self.delete_selected)
        self.reload_listbox_button = Button(self.master, text='Reload List', command=self.list_products)

        self.listbox.grid(row=0, rowspan=3, column=0)
        self.name_label.grid(row=0, column=1)
        self.name_entry.grid(row=0, column=2)
        self.how_much_left_label.grid(row=1, column=1)
        self.how_much_left_entry.grid(row=1, column=2)
        self.cost_label.grid(row=2, column=1)
        self.cost_entry.grid(row=2, column=2)
        self.submit_button.grid(row=3, column=2)
        self.delete_selected_button.grid(row=4, column=2)
        self.error_label.grid(row=5, column=2)
        self.reload_listbox_button.grid(row=4, column=0)

        self.list_products()
        self.master.mainloop()

    def list_products(self):
        self.listbox.delete(0, END)
        Session = sessionmaker(bind=engine)
        session = Session()

        all_products = session.query(Product).all()
        products = []

        for product in all_products:
            products.append(product)
        self.listbox.insert(END, *products)


    def submit_to_database(self):
        self.error_label.configure(text='')
        product_name = self.name_entry.get()
        how_much_left = self.how_much_left_entry.get()
        cost = self.cost_entry.get()

        if product_name == '' or how_much_left == '' or cost == '':
            self.error_label.configure(text='One of the input areas is empty...')
        else:

            Session = sessionmaker(bind=engine)
            session = Session()

            submited_items = Product(name=product_name, how_much_left=how_much_left, cost=cost)

            session.add(submited_items)
            session.commit()


    def delete_selected(self):
        Session = sessionmaker(bind=engine)
        session = Session()

        selected_item_indeces = self.listbox.curselection()
        selected_item_text = self.listbox.get(selected_item_indeces[0])
        selected_item_text_array = selected_item_text.split(',')
        product = session.query(Product).filter_by(name=selected_item_text_array[0]).one()


        session.delete(product)
        session.commit()


def main() -> None:
    MainWindow()

if __name__ == '__main__':
    main()