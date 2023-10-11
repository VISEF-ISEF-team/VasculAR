# VAS - Phần mềm tích hợp học sâu để phân vùng và tái tạo cấu trúc tim 3 chiều cho ứng dụng thực hành y khoa.
# Poster và sơ đồ khối
![](Poster.png)

## Lời cảm ơn
- Cảm ơn bác sĩ Lê Văn Nghĩa (trưởng khoa tim mạch bệnh viện Chợ Rẫy) đã chỉ dẫn những vấn đề quan trọng liên quan tới tim và ảnh chụp cắt lớp.
Cảm ơn bác sĩ Lê Văn Phước (Trưởng khoa Chẩn đoán hình ảnh Bệnh viện Chợ Rẫy) đã thực hiện, tư vấn và hướng dẫn phân vùng bằng tay trên bộ ảnh cắt lớp lòng ngực thô.  
- Cảm ơn bác sĩ Trần Văn Hữu (BS chuyên khoa 2, trưởng khoa ngoại tổng hợp bệnh viện Quận 1) đã tư vấn hướng phát triển và ứng dụng thực tế cho dự án.
- Cảm ơn bác sĩ Lê Thị Phương Nga BS khoa nội, bệnh viện Nguyễn Trãi, TPHCM đã hỗ trợ kiến thức về giãi phẫu lồng ngực, giãi phẫu tim người.
- Cảm ơn anh Đoàn Văn Tuấn (cựu sinh viên trường Đại học Kỹ Thuật Y Tế Hải Dương, khoa chuẩn đoán hỉnh ảnh) đã giúp giới thiệu form khảo sát đến cho các bạn sinh viên khác.  

## Tóm tắt
Trong ngành kỹ thuật chuẩn đoán hình ảnh, chuyên khoa tim mạch, việc đọc hiểu và phân tích chính xác ảnh chụp cắt lớp tim lồng ngực gây nhiều khó khăn cho sinh viên Việt Nam do sự hạn chế về thực hành, kỹ thuật. Điều này gây ra sự giảm sút về số lượng lẫn chất lượng đội ngũ bác sĩ chẩn đoán hình ảnh tiền phẫu tim. Để giải quyết vấn đề này, nhóm phát triển một phần mềm hệ thống có tên VAS trên nền tảng trực tuyến (website) tích hợp các công cụ phân tích nhiều loại ảnh cắt lớp, và tái tạo cấu trúc tim 3D hoàn toàn tự động. Các mô hình học sâu (Deep Learning) đã được nghiên cứu như Unet, VGG, Resnet và các hàm mất mát IoU, Dice Coefficient, Jaccard cho công việc phân vùng (segmentation) hình ảnh cắt lớp tim. Các kiến thức hình học đã được áp dụng như phương trình đường tròn cho quá trình xử lý dữ liệu và hình học không gian cho thuật toán Marching Cubes để trích xuất đặc trưng kết quả phân vùng, tính toán khoảng cách tọa độ lưới và tái tạo mô hình tim 3D trong không gian 3 chiều, kết nối kính VR tăng tính tương tác. Database SQL Alchemy với Python Backend được tích hợp cho nền tảng ứng dụng để hỗ trợ việc lưu trữ ghi chú, phân tích, lên kế hoạch tiền phẫu thuật cho chuyên viên chẩn đoán. Trong quá trình thử nghiệm, mô hình phân vùng đa lớp (multiclass model) sử dụng kiến trúc Unet kết hợp attention vượt xa kiến trúc truyền thống khác, đạt độ chính xác 0.9455 và độ mất mát 0.1414 trên bộ dữ liệu nghiên cứu. Mô hình được biến đổi bằng Tensorflow.js giảm độ nặng, tiết kiệm tài nguyên máy tính trong một lần chạy, tăng tốc độ cho ra kết quả trên nền tảng website dưới 2 phút, nhanh hơn so với các phần mềm khác. 

Từ khóa: tim mạch. mô hình học sâu, phân vùng cắt lớp, tái tạo 3D

## Lý do chọn đề tài
Theo Tổ chức Y tế Thế giới, bệnh tim mạch là nguyên nhân gây tử vong hàng đầu trên toàn cầu (Mendis et al., 2011) [1]. Theo thống kê, Việt Nam có khoảng 200.000 người tử vong vì bệnh tim mạch. Số ca tử vong do các bệnh tim mạch cao hơn cả tử vong do ung thư, hen phế quản và đái tháo đường cộng lại [2]. Trong ca phẫu thuật tim, công tác chuẩn đoán hình ảnh đóng vai trò quan trọng trong việc lập kế hoạch tiền phẫu thuật. Một sai sót trong việc đọc hiểu các ảnh cắt lớp có thể dẫn đến di chứng khó lường, đặc biệt với những ca dị tật, di dạng bẩm sinh (e.g bé Hoàng Lê Khánh Thy – ca ghép tim kỳ lạ [3]). Thế nhưng theo điều tra khảo sát, việc học khoa chuẩn đoán hình ảnh vẫn có nhiều khó khăn cho sinh viên và giảng viên trong công việc giảng dạy. Cụ thể, sinh viên khoa chuẩn đoán hình ảnh ít được tiếp xúc, thực hành với việc đọc và phân tích các hình ảnh cắt lớp thực tế, đa số là tập đọc và học qua sách vở với các tình huống có sẵn. Tuy nhiên thực tế cho thấy tim có thể có nhiều biến chứng bất thường gây khó khăn cho kỹ thuật viên mới ra trường tiếp xúc những ca phân tích hình ảnh cho việc lên kế hoạch tiền phẫu thuật tim. Sinh viên ở Việt Nam hiện nay phần lớn tải các phần mềm nước ngoài để hỗ trợ việc tự nghiên cứu thêm. Tuy nhiên, các phần mềm đó đắt đỏ, chưa tự động hóa hoàn toàn, yêu cầu laptop cấu hình cao và các dữ liệu không tập trung vào nhóm đối tượng người Việt Nam. Để giải quyết nhu cầu này, nhóm nghiên cứu đã chọn đề tài. 


## Mục tiêu nghiên cứu
- Huấn luyện mô hình học sâu phân vùng tim cần đạt độ chính xác xấp xỉ 98-99%, chỉ số Dice Coeffient Score chỉ chấp nhận trên 0.9.
- Lập trình thuật toán tái tạo 3D cần vừa chính xác, nhanh, nhẹ, cho phép người dùng có thể tương tác dễ dàng bằng chuột hoặc bằng mắt kính VR kết nối. Không gian 3D cần có chức năng hiển thị/ẩn từng vùng riêng biệt trong tim.
- Lập trình website hoàn toàn bằng tiếng Việt, hạn chế các tác vụ thừa, có công cụ khó hiểu và tăng cường tính tự động hóa.
- Lập trình thêm cơ sở dữ liệu lưu trữ lại ghi chú của người dùng khi phân tích một file ảnh chụp cắt lớp cụ thể.
## Giả thuyết khoa học
- Nếu nghiên cứu và sản phẩm được hoàn thiện sinh viên sẽ nâng cao khả năng đọc hiểu ảnh cắt lớp, tăng trải nghiệm phân tích dữ liệu thô thực tế, tăng khả năng hình dung, tiết kiệm thời gian. Giảng viên có thể áp dụng nền tảng ứng dụng này trong việc giảng dạy chuẩn đoán hình ảnh trực quan hơn cho sinh viên trong không gian ảo. Điều này giúp cải thiện số lượng và chất lượng bác sĩ chẩn đoán hình ảnh, phục vụ tốt công tác lập kế hoạch tiền phẫu thuật tim, đáp ứng nhu cầu cho hơn 8000 ca phẫu thuật tim tại Việt Nam. [4]
## Nhiệm vụ nghiên cứu
- Nghiên cứu về các định dạng file, đơn vị HounsField, xử lý nhiễu.
- Nghiên cứu về các vùng trong cấu trúc tim và các bệnh lý liên quan đến tim.
- Nghiên cứu các mô hình học sâu tốt cho việc chuẩn đoán hình ảnh y học.
- Nghiên cứu thuật toán hình học không gian tái tạo cấu trúc tim 3 chiều.
- Nghiên cứu môi trường thực tế ảo (VR) cách liên kết với ứng dụng.
## Câu hỏi nghiên cứu
C1: Làm sao để huấn luyện mô hình học sâu đạt kết quả tốt nhất.
C2: Làm sao để xây dựng một website tự động hóa đầy đủ các tính năng, công cụ. 
C3: Làm sao để xây dựng một cơ sở dữ liệu an toàn, bảo mật, lưu trữ xử lý dữ liệu lớn.
## Phương pháp nghiên cứu
- Phương pháp quan sát và điều tra khảo sát.
- Phương pháp thống kê số liệu và đặt giả thuyết.
- Phương pháp thực nghiệm và quy trình thiết kế ứng dụng.
## Tính mới và tính sáng tạo của đề tài
- Nền tảng ứng dụng đầu tiên chạy trên website tại Việt Nam sử dụng các mô hình học sâu ứng dụng cho nhiệm vụ phân tích chuyên sâu về ảnh cắt lớp tim mạch, phần vùng và tái tạo cấu trúc tim 3D một cách tự động hóa hoàn toàn.
- Cùng bác sĩ, chuyên gia chẩn đoán hinh ảnh tạo ra một bộ data mới với số vùng nhiều và chi tiết nhất hiện này (12 vùng), trên thế giới chỉ tối đa 7 vùng. [5]
- Kết nối môi trường thực tế ảo vào trong việc giảng dạy.
