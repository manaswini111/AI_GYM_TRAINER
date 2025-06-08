def get_diet_recommendation(goal, preference):
    if goal.lower() == 'weight loss':
        if preference.lower() == 'veg':
            return "Low-calorie veggies, oats, and lentils"
        else:
            return "Egg whites, chicken breast, veggies"
    elif goal.lower() == 'muscle gain':
        if preference.lower() == 'veg':
            return "Tofu, soy, peanut butter, paneer"
        else:
            return "Chicken, fish, eggs, milk"
    else:
        return "Drink plenty of water, eat balanced food"

# Example use
goal = input("What is your goal (weight loss/muscle gain)? ")
preference = input("Veg or Non-Veg? ")
print(get_diet_recommendation(goal, preference))
