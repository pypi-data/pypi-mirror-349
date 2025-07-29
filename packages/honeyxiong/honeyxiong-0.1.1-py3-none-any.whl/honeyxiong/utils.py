def is_european(brand):
    """Проверяет, является ли марка европейской."""
    european_brands = {"BMW", "Mercedes", "Audi", "Volkswagen", "Volvo", "Porsche", "Ferrari", "Lamborghini"}
    return brand in european_brands

def get_brand_info(brand):
    """Возвращает информацию о марке (заглушка)."""
    return f"Марка {brand} - {'европейская' if is_european(brand) else 'неевропейская'}."