from flask import Flask, render_template, request
import random
app = Flask(__name__)

# Danh sách thực phẩm
'''
foods = {
    'breakfast': [
       # {"name": "Bánh mì", "calories": 250, "price": 20000},
        {"name": "Trứng ốp la", "calories": 150, "price": 10000},
        {"name": "Sữa tươi", "calories": 120, "price": 8000}
    ],
    'lunch': [
        #{"name": "Cơm gà", "calories": 450, "price": 30000},
        {"name": "Bún bò", "calories": 400, "price": 25000},
        {"name": "Cơm tấm", "calories": 350, "price": 22000}
    ],
    'dinner': [
        {"name": "Canh chua cá", "calories": 300, "price": 25000},
        {"name": "Mì xào", "calories": 400, "price": 28000},
        {"name": "Gỏi cuốn", "calories": 200, "price": 15000}
    ]
}
'''

foods = {
        'breakfast': [
            {"name": "Bánh mì", "calories": 250, "price": 20000},
            {"name": "Trứng ốp la", "calories": 150, "price": 10000},
            {"name": "Sữa tươi", "calories": 120, "price": 8000},
            {"name": "Xôi mặn", "calories": 300, "price": 18000},
            {"name": "Bánh bao", "calories": 200, "price": 12000},
            {"name": "Phở", "calories": 350, "price": 30000},
            {"name": "Cháo lòng", "calories": 400, "price": 25000},
            {"name": "Bánh mì ốp la", "calories": 300, "price": 22000}
        ],
        'lunch': [
            {"name": "Cơm gà", "calories": 450, "price": 30000},
            {"name": "Bún bò", "calories": 400, "price": 25000},
            {"name": "Cơm tấm", "calories": 350, "price": 22000},
            {"name": "Phở bò", "calories": 450, "price": 35000},
            {"name": "Bánh canh", "calories": 350, "price": 25000},
            {"name": "Bánh xèo", "calories": 400, "price": 20000},
            {"name": "Gỏi cuốn", "calories": 200, "price": 15000},
            {"name": "Cơm chiên", "calories": 500, "price": 28000}
        ],
        'dinner': [
            {"name": "Canh chua cá", "calories": 300, "price": 25000},
            {"name": "Mì xào", "calories": 400, "price": 28000},
            {"name": "Gỏi cuốn", "calories": 200, "price": 15000},
            {"name": "Mì quảng", "calories": 450, "price": 35000},
            {"name": "Bánh bột lọc", "calories": 250, "price": 15000},
            {"name": "Chả giò", "calories": 300, "price": 20000},
            {"name": "Cơm rang dưa bò", "calories": 500, "price": 30000},
            {"name": "Bánh cuốn", "calories": 350, "price": 22000}
        ]
    }


# Hàm tính tổng calories và chi phí của thực đơn
def suggest_meal(tdee):
    total_calories = 0
    total_cost = 0
    meal_plan = {'breakfast': [], 'lunch': [], 'dinner': []}
    
    # Chọn thực phẩm cho từng bữa ăn sao cho tổng calo gần bằng TDEE và có ít nhất 3 món mỗi bữa
    for meal_time in meal_plan:
        meal_items = foods[meal_time]
        random.shuffle(meal_items)
        meal_count = 0  # Đếm số món ăn trong bữa
        for item in meal_items:
            if total_calories + item['calories'] <= tdee and meal_count < 2:  # Đảm bảo không vượt quá TDEE và có ít nhất 3 món
                meal_plan[meal_time].append(item)
                total_calories += item['calories']
                total_cost += item['price']
                meal_count += 1
                if total_calories >= tdee:
                    break
        
        # Nếu số món trong bữa ăn ít hơn 3, tiếp tục chọn món cho đủ 3 món
        while meal_count < 2:
            additional_item = random.choice(meal_items)  # Chọn món khác nếu chưa đủ số lượng
            if additional_item not in meal_plan[meal_time]:  # Đảm bảo không trùng món
                meal_plan[meal_time].append(additional_item)
                total_calories += additional_item['calories']
                total_cost += additional_item['price']
                meal_count += 1

    return meal_plan, total_cost, total_calories

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Lấy thông tin từ form
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        age = int(request.form['age'])
        gender = request.form['gender']
        activity_level = float(request.form['activity'])

        # Tính BMR
        if gender == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        # Tính TDEE
        tdee = bmr * activity_level

        # Gợi ý thực đơn và tính chi phí
        meal_plan, total_cost, total_calories = suggest_meal(tdee)

        return render_template('index.html', tdee=tdee, meal_plan=meal_plan, total_cost=total_cost, total_calories=total_calories)

    return render_template('index.html', tdee=None, meal_plan=None)

if __name__ == '__main__':
    app.run(debug=True)
