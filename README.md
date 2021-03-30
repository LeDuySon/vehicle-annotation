# vehicle-annotation

### python3 annotate_data.py --txt_path ... --video_path ... --output_path data_rename_class
# Note:
- Red boundingbox: Box chưa đổi lại nhãn
- Blue boundingbox: Box đổi lại nhãn rồi

# Guide:
- Click chuột trái vào box của object( Anh đừng ấn vào vùng box trùng nhau của 2 object ko thì cả 2 thằng đều bị đổi) -> click chuột trái tiếp vào box nhãn -> ấn w (Lưu ý phải ấn vào object trước rồi mới ấn vào box nhãn, không được ấn 2 object hoặc 2 nhãn liên tục do code còn sida :v)
- Để reset box vừa annotate lại thì ấn chuột phải vào bất kì đâu -> ấn w 
- Ấn w để đến frame tiếp theo 
- Ấn q để đến video tiếp theo 
- Sau khi annotate xong sẽ được lưu vào một file txt với tên giống file txt ban đầu -> lưu trong folder output_path với format dạng: id new_class_name
- Sau đấy anh ném e mấy cái file txt đấy em merge lại là được ạ :)))) 
