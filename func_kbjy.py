def calculate_bmr(weight, height, age, gender='male'):
    """
    Рассчитывает базовый метаболизм (BMR) по формуле Миффлина-Сан Жеора

    Args:
        weight: вес в кг
        height: рост в см
        age: возраст в годах
        gender: пол ('male' или 'female')

    Returns:
        float: базовый метаболизм в ккал
    """
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    return bmr


def calculate_tdee(bmr, activity_level):
    """
    Рассчитывает общий расход калорий (TDEE) с учетом уровня активности

    Args:
        bmr: базовый метаболизм
        activity_level: уровень активности (1-5)
          1: Сидячий образ жизни (мало или нет тренировок)
          2: Легкая активность (1-3 тренировки в неделю)
          3: Умеренная активность (3-5 тренировок в неделю)
          4: Высокая активность (6-7 тренировок в неделю)
          5: Экстремальная активность (тяжелые тренировки 2 раза в день)

    Returns:
        float: общий расход калорий в день
    """
    activity_multipliers = {
        1: 1.2,
        2: 1.375,
        3: 1.55,
        4: 1.725,
        5: 1.9
    }
    return bmr * activity_multipliers.get(activity_level, 1.2)

def calculate_kbju(height, weight, age, gender='male', activity_level=3, goal='maintain'):
    """
    Рассчитывает полную суточную норму КБЖУ

    Args:
        height: рост в см
        weight: вес в кг
        age: возраст в годах
        gender: пол ('male' или 'female')
        activity_level: уровень активности (1-5)
        goal: цель ('lose' - похудение, 'maintain' - поддержание, 'gain' - набор)

    Returns:
        dict: словарь с КБЖУ
    """
    # Рассчитываем базовый метаболизм по формуле Миффлина-Сан Жеора
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Уровни активности
    activity_multipliers = {
        1: 1.2,    # Сидячий образ жизни
        2: 1.375,  # Легкая активность
        3: 1.55,   # Умеренная активность
        4: 1.725,  # Высокая активность
        5: 1.9     # Экстремальная активность
    }

    # Рассчитываем общий расход калорий
    tdee = bmr * activity_multipliers.get(activity_level, 1.55)

    # Корректируем калории в зависимости от цели
    goal_multipliers = {
        'lose': 0.85,      # дефицит 15%
        'maintain': 1.0,   # поддержание
        'gain': 1.15       # профицит 15%
    }

    calories = tdee * goal_multipliers.get(goal, 1.0)

    # Рассчитываем белки (1.6-2.2 г/кг в зависимости от цели)
    if goal == 'gain':
        protein_per_kg = 2.2
    elif goal == 'lose':
        protein_per_kg = 2.0
    else:
        protein_per_kg = 1.6

    protein = weight * protein_per_kg
    protein_calories = protein * 4  # 1 г белка = 4 ккал

    # Рассчитываем жиры (25% от общей калорийности)
    fat_calories = calories * 0.25
    fat = fat_calories / 9  # 1 г жира = 9 ккал

    # Рассчитываем углеводы (оставшиеся калории)
    carb_calories = calories - protein_calories - fat_calories
    carbs = carb_calories / 4  # 1 г углевода = 4 ккал

    return {
        'calories': round(calories),
        'protein': round(protein, 1),
        'fat': round(fat, 1),
        'carbs': round(carbs, 1),
        'bmr': round(bmr),
        'tdee': round(tdee)
    }