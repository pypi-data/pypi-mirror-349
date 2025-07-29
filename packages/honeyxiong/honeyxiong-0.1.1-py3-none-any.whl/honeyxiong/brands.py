CAR_BRANDS = [
    "Toyota", "Honda", "Ford", "Chevrolet", "BMW",
    "Mercedes", "Audi", "Volkswagen", "Tesla", "Nissan",
    "Hyundai", "Kia", "Volvo", "Lexus", "Subaru",
    "Mazda", "Jeep", "Porsche", "Ferrari", "Lamborghini"
]

def get_random_brand():
    """Возвращает случайную марку машины."""
    import random
    return random.choice(CAR_BRANDS)

def get_all_brands():
    """Возвращает все доступные марки."""
    return CAR_BRANDS.copy()