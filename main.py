from modules import Json
import csv
import fpdf  # type:ignore
from asyncio import run

from datetime import datetime as dt

FNAME = "./db.json"
FIELDS = [
    "SID",
    "NAME",
    "GENDER",
    "DIET",
    "ALLERGY",
    "IDNUMBER",
    "BIRTH",
    "PHONE",
    "EMGNAME",
    "EMGRELATIONS",
    "EMGPHONE",
    "TIMESTAMP",
]

FIELDS2CHINESE = [
    "學號",
    "姓名",
    "性別",
    "飲食習慣",
    "過敏食物",
    "身分證字號",
    "出生年月日",
    "手機號碼",
    "緊急聯絡人",
    "與學員之關係",
    "緊急連絡人電話",
    "報名時間",
]

GENDER2TXT = {
    "BOY": "男",
    "GIRL": "女",
    "NONBIN": "非二元性別",
}

DIET2TXT = {
    "NORMAL": "葷",
    "VEGAN": "全素",
    "VEGETARIAN": "蛋奶素",
    "OVO-VEGAN": "蛋素",
    "LACTO-VEGAN": "奶素",
    "NO-MEAT": "五辛素",
}

RELATION2TXT = {
    "FATHER": "父",
    "MOTHER": "母",
    "GRANDFATHER": "爺爺/外公",
    "GRANDMOTHER": "奶奶/外婆",
    "OTHERS": "其他",
}


async def datetimeConverter(timestamp):
    time_obj = dt.strptime(timestamp, "%a %b %d %Y %H:%M:%S GMT%z (%Z)")
    return time_obj.strftime("%Y/%m/%d %H:%M:%S")


# from JSON 2 CSV
async def write2CSV():

    data = await Json.aload(FNAME)

    students = data["students"]

    with open("data.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(FIELDS2CHINESE)
        for student_id, student_info in students.items():
            row = [student_id]
            for field in FIELDS[1:]:
                if field == "DIET":
                    row.append(DIET2TXT[student_info.get(field, "")])
                elif field == "GENDER":
                    row.append(GENDER2TXT[student_info.get(field, "")])
                elif field == "EMGRELATIONS":
                    row.append(RELATION2TXT[student_info.get(field, "")])
                elif field == "TIMESTAMP":
                    row.append(await datetimeConverter(student_info.get(field, "")))
                else:
                    row.append(student_info.get(field, ""))
            writer.writerow(row)


# from CSV 2 PDF
async def write2PDF():
    pdf = fpdf.FPDF(orientation="L", unit="mm", format="A4")
    pdf.add_page()
    pdf.add_font("NotoSansTC", "", "NotoSansTC-VariableFont_wght.ttf")
    pdf.set_font("NotoSansTC", "", 8)  # Reduced font size

    # Read data from CSV
    with open("data.csv", "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        data = list(csv_reader)

    # Set up table with adjusted column widths
    col_widths = [20, 20, 10, 15, 15, 25, 20, 25, 20, 25, 25, 35]
    row_height = 7  # Reduced row height

    # Write headers
    for i, field in enumerate(FIELDS2CHINESE):
        pdf.cell(col_widths[i], row_height, field, border=1)
    pdf.ln()

    # Write data
    for row in data:
        for i, field in enumerate(FIELDS2CHINESE):
            cell_text = row[field]
            pdf.cell(col_widths[i], row_height, cell_text, border=1)
        pdf.ln()

    # Save the PDF
    pdf.output("data.pdf")


if __name__ == "__main__":
    run(write2CSV())
    run(write2PDF())
