import tkinter as tk
from tkinter import messagebox, Frame, Canvas, Scrollbar
from lostFind.class_find import LostItemFinder as LIT
import pyperclip

def search_item():
    findItem = entry.get().rstrip()
    distinct = entryDistinct.get().rstrip()
    startDate = entryDate.get()
    endDate = entryDate2.get()  
    if not findItem or not distinct or not startDate:
        messagebox.showwarning("입력 오류", "검색할 아이템을 입력하세요.")
        return
    lostMyItem = LIT(findItem, distinct, startDate, endDate)
    lostMyItem.open_website("https://www.lost112.go.kr/find/findList.do")
    lostMyItem.input_item()
    lostMyItem.select_date()
    results = lostMyItem.search_items()
    lostMyItem.close_browser()
    
    clear_buttons()  # 기존 버튼 지우기
    create_buttons(results)  # 새로운 버튼 생성

def clear_buttons():
    for widget in button_frame.winfo_children():
        widget.destroy()

def create_buttons(results):
    for result in results:
        button = tk.Button(button_frame, text=result, command=lambda r=result: copy_to_clipboard(r))
        button.pack(fill=tk.X, pady=2)

def copy_to_clipboard(selected_text):
    pyperclip.copy(selected_text[6:])  # 텍스트를 클립보드에 복사
    messagebox.showinfo("알림", "복사완료")

# Tkinter UI 설정
root = tk.Tk()
root.title("물건 검색기")

frame = tk.Frame(root)
frame.pack(pady=20)

# 물건
label = tk.Label(frame, text="찾을 물건:")
label.pack()
entry = tk.Entry(frame)
entry.pack()

# 특이사항
label_distinct = tk.Label(frame, text="찾을 물건의 특이사항:")
label_distinct.pack()
entryDistinct = tk.Entry(frame)
entryDistinct.pack()

# 날짜
label_date = tk.Label(frame, text="시작날짜(ex 20240427)")
label_date.pack()
entryDate = tk.Entry(frame)
entryDate.pack()

label_date2 = tk.Label(frame, text="종료날짜(ex 20240805)")
label_date2.pack()
entryDate2 = tk.Entry(frame)
entryDate2.pack()

search_button = tk.Button(frame, text="검색", command=search_item)
search_button.pack(pady=10)

# 스크롤 가능한 영역 설정
canvas = Canvas(root)
scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
button_frame = Frame(canvas)

button_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=button_frame, anchor="nw")

canvas.config(yscrollcommand=scrollbar.set)

canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

center_frame = Frame(button_frame)
center_frame.config(pady =10)

button_frame.pack_propagate

root.mainloop()
