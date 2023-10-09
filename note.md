# Segmentation Speculations
## I. Các vùng cần phân khu và các lưu ý kèm theo

1. Tâm nhĩ trái (Left Atrium): ở dưới động mạch phổi, nhận máu giàu oxi từ động mạch phổi

2. Tâm nhĩ phải (Right Atrium): gần tĩnh mạch chủ trên, tĩnh mạch chủ trên (Superiror Vena Cava) sẽ đổ máu thiếu oxi (deoxygenated blood) vào tâm thất phải (Right Ventricle)

3. Tâm thất trái (Left Ventricle): dưới nhĩ trái, ngăn bởi van 2 lá (Mitral Valve)

4. Tâm thất phải (Right Ventricle): dưới nhĩ phải, ngăn bởi van 3 lá (Tricuspid Valve)

5. Van tim:

    5.1. Van 2 lá (Mitral Valve): nằm ở buồng tim trái, một đường cơ đậm nối giữa nhĩ trái và thất trái.
    
    5.2. Van 3 lá (Tricuspid Valve), nối giữa nhĩ phải và nhĩ trái một đường cơ không đậm bằng van 3 lá, nối giữa nhỉ phải và thất phải.

6. Màng tim (Pericardium): có lớp dịch sinh lý để tim co bóp (có thể bị tràn), màng mỏng bao bọc quanh

7. Cung động mạch chủ (Arch of Aeorta): có hình vòng cung

8. Động mạch chủ (Aorta): sẽ chia làm 2 phần ở cung động mạch chủ

9. Tĩnh mạch chủ trên (Superior Vena Ceva) 

10. Tĩnh mạch chủ dưới (Inferior Vena Ceva) 

11. Động mạch phổi (Pulmonary artery): hình ống, dài, khi nhìn từ trên xuống thì sẽ nằm trên nhĩ trái.

### II. Color mapping:

1. Left atrium: #f1d691
2. Left ventricle: #b17a65
3. Right atrium: #6fb8d2
4. Right ventricle: #d8654f
5. Mitral (bicuspid) valve: #dd8265
6. Tricuspid valve: #90ee90
7. Pericardium: #dcf514
8. Aeorta: #fc8184
9. Superior Vena Ceva: #0d05ff
10. Inferior Vena Ceva: #e6dc46
11. Background: #c8c8eb -> không hiển thị khi xuất file .nii.gz
12. Aeortic arch: #fa0101
13. Pulmonary artery: #f4d631


1 left_atrium 128 174 128 255
2 left_ventricle 241 214 145 255
3 right_atrium 111 184 210 255
4 right_ventricle 216 101 79 255
5 bicuspid_valve 216 101 79 255
6 tricuspid_valve 144 238 144 255
7 pericardium 220 245 20 255
8 aeorta 252 129 132 255
9 SVC 13 5 255 255
10 IVC 230 220 70 255
11 background 0 0 0 255
12 aeortic_arch 250 1 1 255
13 pulmonary_artery 244 214 49 255

### III. Các góc nhìn trong chụp CT

1. Axial: Chụp từ trên xuống (góc nhìn từ đầu bệnh nhân nhìn xuống). Hình ảnh là hình chiếu bằng của vật. Mặt phẳng cắt là một mặt phẳng nằm ngang, vuông góc với bệnh nhân.

2. Sagital: Chụp từ 1 bên (trái / phải) về bên còn lại. Hình ảnh là hình chiếu cạnh của vật. Mặt phẳng cắt là mặt phẳng dọc, vuông góc với bệnh nhân và vuông góc với mặt axial.

3. Coronal: Chụp từ 1 phía (trước / sau) về phía còn lại. Hình ảnh là hình chiếu đứng của vật. Mặt phẳng cắt là mặt phẳng dọc, song song với bệnh nhân.


### IV. Cửa sổ CT
* Threshold + Window Width for HounsField Filtering
    -   Các phần mềm được sử dụng thực tế ở bệnh viện nó đang như nào ?
    -   Nếu được cải tiến thì sẽ cải tiến điểm gì ?
    -   Có thật sự hữu ích hay không ?
    -   Các hướng phát triển thêm
    -   Hỏi cách dựng mô hình 3D
    -   Hỏi các vùng NÊN được highlight và chú ý nhiều đến
    -   Hỏi cách đọc và segment CT
    -   Xin dataset

