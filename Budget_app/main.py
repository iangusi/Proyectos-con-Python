import budget
from budget import create_spend_chart

food = budget.Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
clothing = budget.Category("Clothing")
food.transfer(50, clothing)
clothing.withdraw(25.55)
clothing.withdraw(100)
auto = budget.Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(15)
save = budget.Category("Saving")
food.transfer(500,save)
auto.transfer(500,save)
save.withdraw(800, "need to buy a phone")

print(food)
print(clothing)
print(auto)
print(save)

print(create_spend_chart([food, clothing, auto, save]))
