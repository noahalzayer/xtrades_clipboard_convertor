import datetime
import tkinter as tk

MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']


class XtradesClipboardConvertor(object):
    """
    Main Window class
    """
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Xtrades Clipboard Convertor')
        self.window.rowconfigure(0, minsize=30, weight=0)
        self.window.columnconfigure(0, minsize=80, weight=1)
        self.window.rowconfigure(1, weight=1)

        self.output = tk.Text(self.window, state='disabled', wrap=tk.NONE)
        self.buttons_frame = tk.Frame(self.window, relief=tk.RAISED, bd=2)
        self.clip_btn = tk.Button(self.buttons_frame, text='Parse From Clipboard', command=lambda: self.parse(clip=True))
        self.field_btn = tk.Button(self.buttons_frame, text='Parse From Field', command=lambda: self.parse(clip=False))
        self.field = tk.Entry(self.buttons_frame)
        self.buttons_frame.columnconfigure(2, minsize=200, weight=1)

        self.clip_btn.grid(row=0, column=0, sticky='ew', padx=5)
        self.field_btn.grid(row=0, column=1, sticky='ew', padx=5)
        self.field.grid(row=0, column=2, sticky='nsew', padx=5)

        self.buttons_frame.grid(row=0, column=0, sticky='nsew')
        self.output.grid(row=1, column=0, sticky='nsew')

        self.window.mainloop()

    def output_add(self, txt):
        """
        Adds to the output window
        Args:
            txt (str): The text to add
        """
        self.output.configure(state='normal')
        self.output.insert('end', '{}\n\n'.format(txt))
        self.output.configure(state='disabled')
        self.output.see(tk.END)

    def parse(self, clip):
        """
        Takes the play format from xtrades and converts to a format recognmizable by Thinkorswim
        Args:
            clip (bool): Determines whether to draw the incoming text from the clipboard or the text field
        Returns:
            str: The parsed result
        """
        if clip:
            txt = self.window.clipboard_get()
        else:
            txt = self.field.get()

        txt = txt.strip()

        self.output.configure(state='normal')
        self.output.delete('1.0', tk.END)
        self.output_add('Raw Input:\n\t{}'.format(txt))

        txt = txt.replace('@ ', '@').replace('/ ', '/').replace(' /', '/').replace('  ', ' ').replace('$', '')

        if not len(txt.split()) == 5:
            self.outputd_add('\n################\nERROR - Unable to split play in to proper components.\n'
                            'The format needs to be "Action (BTO, STO) Ticker (TSLA, AAPL) Expiration (10/28) Stike (125c) Price (@2.50)"')
            return

        action, symbol, exp, strike, price = txt.split()

        action = 'BUY' if action.lower().startswith('bt') else 'SELL'
        self.output_add('Action:\n\t{}'.format(action))

        symbol = symbol.strip().upper()
        self.output_add('Ticker:\n\t{}'.format(symbol))

        if not exp.count('/') == 1:
            self.output_add('\n################\nERROR - Incorrect Date Format ({}). The format needs to be Month/Day. ex-08/28'.format(exp))
            return

        # Figure out the expiration date
        day = exp.split('/')[1]
        self.output_add('Day:\n\t{}'.format(day))

        month = MONTHS[int(exp.split('/')[0]) - 1]
        self.output_add('Month:\n\t{}'.format(month))

        year = str(datetime.date.today().timetuple()[0])[2:]

        # Mark as next year if the exp month is before the current month
        if int(exp.split('/')[0]) < datetime.date.today().timetuple()[1]:
           year = str(int(year) + 1)

        self.output_add('Year:\n\t{}'.format(year))

        date = '{} {} {}'.format(day, month, year)

        if not strike.lower().endswith('c') and not strike.lower().endswith('p'):
            self.output_add('\n################\nERROR - Incorrect Strike Format ({}). The format needs to be <Price><Type>. ex-125c'.format(strike))
            return

        parsed_strike = strike.replace('c', 'C').replace('C', ' CALL').replace('p', 'P').replace('P', ' PUT')
        self.output_add('Strike:\n\t{}'.format(parsed_strike))

        order = '{} +1 {} 100 {} {} {} LMT'.format(action, symbol, date, parsed_strike, price)
        self.output_add('Full Order:\n\t{}'.format(order))

        self.window.clipboard_clear()
        self.window.clipboard_append(order)
        self.window.update()

        self.output_add('------------\n\nSuccessfully read \t"{}" from clipboard\nReplaced with "{}"\n\n'
                        'May the charts be with you.'.format(txt, order))


XtradesClipboardConvertor()
