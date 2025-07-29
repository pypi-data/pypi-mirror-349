import random

def generate_plate(region="RU"):
    """Генерирует случайный номер (формат: X123XX 123)."""
    letters = "АВЕКМНОРСТУХ"
    num = random.randint(100, 999)
    let1 = random.choice(letters)
    let2 = random.choice(letters)
    let3 = random.choice(letters)
    return f"{let1}{num}{let2}{let3} {region}"

def generate_custom_plate(pattern="A999AA"):
    """Генерирует номер по заданному шаблону (A=буква, 9=цифра)."""
    plate = []
    for char in pattern:
        if char == "A":
            plate.append(random.choice("АВЕКМНОРСТУХ"))
        elif char == "9":
            plate.append(str(random.randint(0, 9)))
        else:
            plate.append(char)
    return "".join(plate)