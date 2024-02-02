def approximate_integral(x, y):
    """
    Xấp xỉ tích phân của đồ thị y=f(x) dựa trên các điểm (x, y).
    """
    integral_approximation = 0
    n = len(x)

    for i in range(1, n):
        # Chiều rộng của mỗi phần giữa các điểm x
        delta_x = x[i] - x[i-1]
        
        # Diện tích của hình chữ nhật: chiều rộng * chiều cao
        area = delta_x * y[i-1]
        
        # Cộng diện tích vào xấp xỉ tích phân
        integral_approximation += area

    return integral_approximation

def calculate_volume(x, y):
    """
    Tính thể tích của vật 3D dựa trên các điểm (x, y).
    """
    integral_approximation = approximate_integral(x, y)
    return integral_approximation

# Ví dụ minh họa
x_points = [1, 2, 3, 4, 5]
y_areas = [10, 15, 8, 12, 20]

volume = calculate_volume(x_points, y_areas)
print("Thể tích của vật 3D là:", volume)
