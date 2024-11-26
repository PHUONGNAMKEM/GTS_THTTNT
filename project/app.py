from flask import Flask, render_template, jsonify, request
import math

app = Flask(__name__)

# Danh sách các địa điểm
# locations = [
#     {"name": "Bảo tàng Mỹ thuật TP.HCM", "address": "Bảo tàng Mỹ thuật TP.HCM", "latitude": 10.769893, "longitude": 106.699264},
#     {"name": "Bảo tàng Thành phố Hồ Chí Minh", "address": "Bảo tàng Thành phố Hồ Chí Minh", "latitude": 10.775979, "longitude": 106.699616},
#     {"name": "Lăng Tả quân Lê Văn Duyệt", "address": "Lăng Ông - Bà Chiểu", "latitude": 10.802130, "longitude": 106.697071},
#     {"name": "Chùa Ngọc Hoàng", "address": "Chùa Ngọc Hoàng", "latitude": 10.791990, "longitude": 106.698185},
#     {"name": "Chùa Bà Thiên Hậu", "address": "Chùa Bà Thiên Hậu", "latitude": 10.824918, "longitude": 106.685290},
# ]


locations = [
            {
                "address": "Bảo tàng Mỹ thuật TP.HCM",
                "name": "Bảo tàng Mỹ thuật TP.HCM",
                "latitude": 10.769893229296022,
                "longitude": 106.69926378493048 
            },
            {
                "address": "Bảo tàng Thành phố Hồ Chí Minh",
                "name": "Bảo tàng Thành phố Hồ Chí Minh",
                "latitude": 10.775978692274064,
                "longitude": 106.69961645071125 
            },
            {
                "address": "Lăng Tả quân Lê Văn Duyệt (Lăng Ông - Bà Chiểu)",
                "name": "Lăng Tả quân Lê Văn Duyệt (Lăng Ông - Bà Chiểu)",
                "latitude": 10.802130314865222,
                "longitude": 106.69707050507084 
            },
            {
                "address": "CHÙA NGỌC HOÀNG",
                "name": "CHÙA NGỌC HOÀNG",
                "latitude": 10.791989934733742,
                "longitude": 106.69818480764916 
            },
            {
                "address": "Chùa Bà Thiên Hậu",
                "name": "Chùa Bà Thiên Hậu",
                "latitude": 10.824918365580874,
                "longitude": 106.68528986651943 
            },
            {
                "address": "Ủy ban Nhân dân Thành phố Hồ Chí Minh",
                "name": "Ủy ban Nhân dân Thành phố Hồ Chí Minh",
                "latitude": 10.776601242663828,
                "longitude": 106.70090551452533 
            },
            {
                "address": "Bưu điện Thành phố Hồ Chí Minh",
                "name": "Bưu điện Thành phố Hồ Chí Minh",
                "latitude": 10.779878166040378,
                "longitude": 106.69995864731223 
            },
            {
                "address": "Nhà thờ Đức Bà Sài Gòn",
                "name": "Nhà thờ Đức Bà Sài Gòn",
                "latitude": 10.779742129400322,
                "longitude": 106.69903701880996 
            },
            {
                "address": "Chợ Bình Tây",
                "name": "Chợ Bình Tây",
                "latitude": 10.749655213007767,
                "longitude": 106.65102842695318 
            },
            {
                "address": "Chợ Bến Thành",
                "name": "Chợ Bến Thành",
                "latitude": 10.772488517534407,
                "longitude": 106.69805791035111 
            },
            {
                "address": "Bến Nhà Rồng - Bảo Tàng Hồ Chí Minh (Chi nhánh TP.HCM)",
                "name": "Bến Nhà Rồng - Bảo Tàng Hồ Chí Minh",
                "latitude": 10.76823090834184,
                "longitude": 106.70680404487891 
            },
            {
                "address": "Thảo Cầm Viên Sài Gòn",
                "name": "Thảo Cầm Viên Sài Gòn",
                "latitude": 10.78754466508065,
                "longitude": 106.70527963295666 
            },
            {
                "address": "Dinh Độc Lập",
                "name": "Dinh Độc Lập",
                "latitude": 10.77696289643182,
                "longitude": 106.69535990362665 
            }
        ];


# Hàm tính khoảng cách giữa hai điểm (Haversine formula)
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # bán kính Trái Đất (km)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Thuật toán Greedy TSP
def greedy_tsp(locations, start_index):
    visited = [False] * len(locations)
    path = []
    current_index = start_index

    for _ in range(len(locations)):
        path.append(locations[current_index])
        visited[current_index] = True
        next_index = -1
        min_distance = float('inf')

        for i, location in enumerate(locations):
            if not visited[i]:
                distance = calculate_distance(
                    locations[current_index]["latitude"],
                    locations[current_index]["longitude"],
                    location["latitude"],
                    location["longitude"]
                )
                if distance < min_distance:
                    min_distance = distance
                    next_index = i

        current_index = next_index if next_index != -1 else current_index

    return path

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/locations", methods=["GET"])
def get_locations():
    return jsonify(locations)

@app.route("/api/journey", methods=["POST"])
def calculate_journey():
    data = request.json
    start_index = data.get("start_index", 0)
    path = greedy_tsp(locations, start_index)
    return jsonify(path)

if __name__ == "__main__":
    app.run(debug=True)
