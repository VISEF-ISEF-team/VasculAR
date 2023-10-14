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

### V. Nghiên cứu chuyên sâu các vùng
CT pulmonary angiogram protocol (CTPA): injection di chuyển từ động mạch phổi (pulmonary arteries) vào phổi (lungs) trở về tĩnh machhj phổi (pulmonary veins) vào tim trái và vào trong động mạch chủ (aorta) và những động mạch khác. Việc này được dùng để đánh giá mạch máu (vasculature). Còn có những protocols khác như low-dose CT lồng ngực và high-resolution CT lồng ngực.

- Thoracic cavity: khoang ngực được bao quanh bởi vách ngực (chest walls) bao gồm xương và cơ.
    - Thoracic inlet: phần đầu từ trên xuống, có lỗ nhỏ màu đen bao quan bởi xương sườn (ribs)
    - Thoracic outlet: đóng bởi cơ hoành (diaphragm) và xương ức (sternum)
    - Mediastinum: phân chia trung thất bằng dùng fibrous perdicardium (màng bao tim) làm mốc (landmark) 
    - Trachea: khí quản + esophagus: thực quản (ở Thoracic inlet)

- Anterior mediastinum: trước màng tim, chứa thyroid, hạch bạch huyết (lymph nodes), thyroid
    - Thymic lesions / Thymoma: tổn thương tuyến ức, u tuyến ức
- Superior / Inferior Vena Cava: Tĩnh mạch chủ trên / tĩnh mạch chủ dưới
- Right atrial appendage
- Right Ventricle: tâm thất phải pumps máu vào trong động mạch phổi (pulmonary arteries) sau đó vào pulmonary trunk và hai cuốn phổi trái phải. Sau đó máu từ cuốn phổi ra phổi ròi lại trở ngược vào tĩnh mạch phổi
- Moderator band: from the interventricular septum
- Left atrium + left atrial appendage --> common position cho blood clots (khối máu, cục máu) hình thành. Tâm nhĩ trái thường <= 4 centimeters trong AP dimensions
- Left ventricle: thicker wall comparted to the right ventricle. Tâm thất trái pumps máu vào trong động mạch chủ (aorta) --> aortic valve --> ascending aorta
- Ascending aorta + Descending aorta = Aortic arch

- Coronary arteries (động mạch vành):
    - Left
    - Circumflex
    - right
- Brachiocephalic veins x 2 --> Superior Vena Cava --> Right atrium
- Azygous arch: join the superior vena cava
- Coronary Sinus: Xoang Vành - the largest cardiac vein (tĩnh mạch tim lớn nhất) --> rains into right atrium (chạy vào tâm nhĩ phải như là SVC)

### Cardiovascular Diseases Reseearch
- MRI (protons) có thể phân biệt thiếu màu (ischemic) và không thiếu máu (non-ischemic) của rối loạn chức năng tâm thất(ventricular dysfunction)
- CT (X-rays): non-invasively delinieate coronary anatomy (Giải phẫu mạch vành không xâm lấn)
- Imaging modalities available to assess coronary artery diseases (CAD) includes echocardiography and nuclear cardiac imaging --> MRI and CT becomes an option.

### Coronary artery images vs Ct chest for CAD diagnosis
There is a difference between coronary artery images and CT chest images. Coronary artery images are obtained by using a specific type of CT scan that focuses on the heart and its blood vessels. CT chest images are more general and show the lungs, ribs, and other structures in the chest. Coronary artery images are more useful for diagnosing coronary artery disease (CAD) such as stenosis, which is a narrowing or blockage of the arteries that supply blood to the heart.

To diagnose CAD, doctors may use different methods depending on the symptoms, risk factors, and availability of the tests. Some of the common methods are:

- Coronary angiogram: This is an invasive procedure that involves inserting a thin tube (catheter) into a blood vessel, usually in the wrist or groin, and guiding it to the heart. A dye is injected through the catheter and X-rays are taken to show the blood flow and any blockages in the coronary arteries⁵.
- CT coronary angiogram: This is a noninvasive procedure that uses a CT scan to create detailed images of the heart and its blood vessels. A dye may be given by IV to make the arteries more visible¹⁴.
- Cardiac catheterization: This is similar to a coronary angiogram, but it can also measure the pressure and oxygen levels in the heart chambers and blood vessels. It can also be used to treat some types of CAD by inflating a balloon or placing a stent to open up a blocked artery⁵.
- Echocardiogram: This is a noninvasive test that uses sound waves to create pictures of the heart and its valves. It can show how well the heart is pumping and if there is any damage to the heart muscle or valves¹.
- Electrocardiogram (ECG or EKG): This is a quick and painless test that measures the electrical activity of the heart. It can show how fast or slow the heart is beating and if there are any abnormal rhythms or signs of a heart attack¹.
- Exercise stress test: This is a test that monitors the heart's response to physical activity. It can be done by walking on a treadmill or riding a stationary bike while having an ECG, echocardiogram, or nuclear stress test. A nuclear stress test uses a radioactive tracer to show how blood flows to the heart at rest and during stress¹².
- Chest X-ray: This is a simple and common test that uses X-rays to create images of the chest. It can show the size and shape of the heart and lungs and if there is any fluid or inflammation in the chest².

The best method for diagnosing CAD depends on many factors, such as the severity of symptoms, medical history, risk factors, and availability of tests. Your doctor will recommend the most appropriate test for you based on your individual situation.

Source:
(1) Coronary artery disease - Diagnosis and treatment - Mayo Clinic. https://www.mayoclinic.org/diseases-conditions/coronary-artery-disease/diagnosis-treatment/drc-20350619.
(2) CT coronary angiogram - Mayo Clinic. https://www.mayoclinic.org/tests-procedures/ct-coronary-angiogram/about/pac-20385117.
(3) CT scans of the heart - Heart Matters magazine - BHF. https://www.bhf.org.uk/informationsupport/heart-matters-magazine/medical/tests/ct-scans-of-the-heart.
(4) Heart CT Scan: Purpose, Procedure & Risks - Cleveland Clinic. https://my.clevelandclinic.org/health/diagnostics/16834-cardiac-computed-tomography.
(5) CT Scan for Coronary Artery Disease > Fact Sheets - Yale Medicine. https://www.yalemedicine.org/conditions/ct-scan-for-coronary-artery-disease.
(6) Coronary Artery Disease: How This Is Diagnosed - Healthline. https://www.healthline.com/health/how-is-coronary-artery-disease-diagnosed.
(7) Coronary Artery Disease Diagnosis - Verywell Health. https://www.verywellhealth.com/diagnosing-coronary-artery-disease-1745913.


### Coronary Artery Diseases (CADs) with CT/MRI
It is possible to diagnose the coronary artery diseases (CAD) with CT chest images by segmentation and reconstruction. CT chest images can show the internal structures of the heart and lungs, as well as the coronary arteries that supply blood to the heart. By using deep learning techniques, such as convolutional neural networks (CNNs), the coronary arteries can be segmented from the CT chest images and reconstructed into 3D models. This can help to detect and quantify the degree of stenosis, which is a narrowing or blockage of the arteries that can cause reduced blood flow and lead to angina, heart attack, or heart failure⁶⁷.

However, there are also some limitations with this approach. First, CT chest images may not have sufficient resolution or contrast to capture the fine details of the coronary arteries, especially for small or distal branches. Second, CT chest images may suffer from motion artifacts due to cardiac and respiratory movements, which can affect the accuracy of segmentation and reconstruction. Third, CT chest images expose the patient to radiation, which may increase the risk of cancer in the long term. Therefore, CT chest images should be used with caution and only when clinically indicated²³⁹.

Source:
(1) Deep Learning for Cardiac Image Segmentation: A Review. https://www.frontiersin.org/articles/10.3389/fcvm.2020.00025/full.
(2) Segmentation of Coronary Arteries from CTA axial slices using Deep .... https://ieeexplore.ieee.org/document/8929260/.
(3) Cardiovascular computed tomography imaging for coronary artery disease .... https://heart.bmj.com/content/heartjnl/early/2022/01/12/heartjnl-2021-320265.full.pdf.
(4) Using CT Scan to Diagnose Heart Disease - WebMD. https://www.webmd.com/heart-disease/diagnosing-heart-disease-cardiac-computed-tomography-ct.
(5) Frontiers | Artificial Intelligence in Coronary CT Angiography: Current .... https://www.frontiersin.org/articles/10.3389/fcvm.2022.896366/full.
(6) CT Scan for Coronary Artery Disease > Fact Sheets - Yale Medicine. https://www.yalemedicine.org/conditions/ct-scan-for-coronary-artery-disease.
(7) Coronary Computed Tomography Angiography (CCTA). https://www.hopkinsmedicine.org/health/treatment-tests-and-therapies/coronary-computed-tomography-angiography-ccta.
(8) CT coronary angiogram - Mayo Clinic. https://www.mayoclinic.org/tests-procedures/ct-coronary-angiogram/about/pac-20385117.
(9) ImageCAS-A-Large-Scale-Dataset-and-Benchmark-for-Coronary-Artery .... https://github.com/XiaoweiXu/ImageCAS-A-Large-Scale-Dataset-and-Benchmark-for-Coronary-Artery-Segmentation-based-on-CT.
(10) undefined. https://doi.org/10.3389/fcvm.2020.00025.
