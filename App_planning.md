Application Structure and organization:

# I. MAIN 
## MENU BAR
### Setting
### Preferences 
--> color themes + languages

### Help 
* Website 
* Guildance 
-> Functions + Defect + 3D + AR/VR

## LEFT HAND FUNCTIONS
## tabview (Step Guildlines)
### 1. Basic functions 
- Color maps
- Support functions
- Drawing functions -> (rectangle, circle, line, brush, erase -> size of brush -> color of brush, ROI can be edited)

    rectangle 1 --> data:
        'rectangle_1': {
            'cord': 'x1, y1, x2, y2',
            'slice': 'num_slice',
            'color': 'color_hex'
            'note': {
                'text': 'text'
                'cord': ''x1, y1'
            }
        },
        'line_1' : {
            'distance': '2.2mm',
            'coord' : 'x1, y1, x2, y2',
            'slice': 'num_slice'
            'note': {
                'text': 'text'
                'cord': ''x1, y1'
            }
        }
        
    brush --> can be erased
    ROI --> can be transformed (can be either circle or rectangle with rotated orientation)
    From the filled-color pixel --> added as brush --> coutour --> added as continuouse edited lined (polygon)
    
- HounsField Unit
- Brightness / Contrast
- Cropping / Axis with ruler + ROI

### 2. Deep learning analysis
- tools for edit, note, save analysis

### 3. Segmentation + 3D reconstruction -> preoperative planning
- optional --> volumn calculation
- vedo + note + rulers for measurement

### 4. VR and AR technology for planning
- Database web + sketchlab

### CANVAS VIEW
- three columns --> can add text to image and take snapshot
                --> khoanh vùng với nhiều shape (vuông, tròn) --> hiện lên bảng ghi chú text (có hoặc không)
                --> Sau khi AI tự khoanh vùng và trả lại ảnh hiện thị khung có thể edit (bỏ, chấp nhận, ghi chú thêm)
                --> tạo thử database lưu những phân tích của mình trên ảnh và hiển thị lại đúng slice đó 
                --> Trên cavas có thước đo dọc thể hiện khoảng cách hiện tại
                --> zoom in out and move


# II. Database Management 
- Patient id
- Patient Name
    times:
    - Modality
    - Date
    - Note analysis --> pdf
- Retrieve new database from cloud
- Update (push new analysis) to json