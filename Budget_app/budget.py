class Category:

  def __init__(self, name):
    self.name = name
    self.ledger = []

  def __str__(self):
    width = 30
    space_name = len(self.name)

    name_start = (width-space_name)//2

    rows = '*'*name_start + self.name + '*'*(width-name_start-space_name) + '\n'

    for move in self.ledger:
        space_amount = len("{:.2f}".format(move['amount']))
        space_description = len(move['description'])

        space_void = width-space_description-space_amount

        if space_void < 1:
            rows += move['description'][:(width-1-space_amount)] + ' '
        else:
            rows += move['description'] + ' '*space_void
            
        rows += "{:.2f}".format(move['amount']) + '\n'

    total = self.get_balance()

    rows += "Total: {:.2f}".format(total)

    return rows
  
  def deposit(self, amount, description=''):
    self.ledger.append({'amount':amount,'description':description})

  def withdraw(self, amount, description=''):
    if self.check_funds(amount):
        self.ledger.append({'amount':-1*amount,'description':description})
        return True
    return False

  def get_balance(self):
    money = 0
    for move in self.ledger:
        money += move['amount']
    return money

  def transfer(self, amount, category):
    if self.check_funds(amount):
        self.ledger.append({'amount':-1*amount,'description':f'Transfer to {category.name}'})
        category.deposit(amount,f'Transfer from {self.name}')
        return True
    return False

  def check_funds(self, amount):
    if self.get_balance() >= amount:
        return True
    return False

def create_spend_chart(categories):
    grafico = "Percentage spent by category"

    category_bills = []
    total_bills = 0

    len_name = 0
    
    for category in categories:
        len_name = len(category.name) if len(category.name) > len_name else len_name
        bills = 0
        for move in category.ledger:
            if move['amount'] < 0:
                bills -= move['amount']
        category_bills.append(bills)
        total_bills += bills

    category_percentage = []

    for spends in category_bills:
        category_percentage.append((spends*100)//total_bills)
    
    for percentage in range(100,-10,-10):
        grafico += '\n'+ ' '*(3-len(str(percentage))) + (str(percentage)) + '|'

        for _percentage in category_percentage:
            grafico += ' o ' if _percentage >= percentage else '   '

    grafico += '\n    ' + '-'*(len(categories)*3+1)

    for index in range(len_name):
        grafico += '\n    '
        for category in categories:
            try:
                grafico += f' {category.name[index]} '
            except:
                grafico += f'   '
        
    
    return grafico



