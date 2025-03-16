from langchain_core.tools import tool
from utils.AppConfig import AppConfig

_ = AppConfig()  #we just have to load the env


@tool
def calculate_discount(price: float, discount_percentage: float) -> float:
    """
    Calculates the final price after applying a discount.

    Args:
        price (float): The original price of the item.
        discount_percentage (float): The discount percentage (e.g., 20 for 20%).

    Returns:
        float: The final price after the discount is applied.
    """
    if not (0 <= discount_percentage <= 100):
        raise ValueError("Discount percentage must be between 0 and 100")

    discount_amount = price * (discount_percentage / 100)
    final_price = price - discount_amount
    return final_price

#langchain tool decorator has converted the python function into Runnable
#It means they can be invoked using invoke() method.
#we can pass a dictionary to invoke() method with keys matching
#the names of parameters that the function expects.
#we can also print name and description and args of the tool
print(calculate_discount.name)
print(calculate_discount.description)
print(calculate_discount.args)
print(calculate_discount.invoke({"price":100.25, "discount_percentage": 15}))

