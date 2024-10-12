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
    "簽名",
    # "性別",
    # "飲食習慣",
    # "過敏食物",
    # "身分證字號",
    # "出生年月日",
    # "手機號碼",
    # "緊急聯絡人",
    # "與學員之關係",
    # "緊急連絡人電話",
    # "報名時間",
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

DEPART2CSVFILENAME = {
    "14": "CSE.csv",  # 資工A
    "15": "CSE.csv",  # 資工B
    "16": "IM.csv",  # 資管A
    "17": "IM.csv",  # 資管B
    "18": "IC.csv",  # 資傳A(設計組)
    "20": "IC.csv",  # 資傳B(科技組)
    "33": "CSE.csv",  # 資工C
    "35": "IN.csv",  # 資英
}

FILENAMES = ["CSE", "IM", "IC", "IN"]


async def datetimeConverter(timestamp):
    return
    time_obj = dt.strptime(timestamp, "%a %b %d %Y %H:%M:%S GMT%z (%Z)")
    return time_obj.strftime("%Y/%m/%d %H:%M:%S")


async def init_csv():

    for filename in FILENAMES:
        with open(filename + ".csv", "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(FIELDS2CHINESE)


# from JSON 2 CSV
async def write2CSV():

    data = await Json.aload(FNAME)

    students = data["students"]

    for sid, info in students.items():

        depart = sid[3:5]
        filename = DEPART2CSVFILENAME[depart]
        with open(filename, "a+", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            # writer.writerow(FIELDS2CHINESE)
            row = [sid]
            for field in FIELDS[1:]:
                if field != "NAME":
                    continue
                else:
                    row.append(info.get(field, ""))
                    continue
                if field == "DIET":
                    row.append(DIET2TXT[info.get(field, "")])
                elif field == "GENDER":
                    row.append(GENDER2TXT[info.get(field, "")])
                elif field == "EMGRELATIONS":
                    row.append(RELATION2TXT[info.get(field, "")])
                elif field == "TIMESTAMP":
                    continue
                    # row.append(await datetimeConverter(info.get(field, "")))
                else:
                    row.append(info.get(field, ""))
            writer.writerow(row)


# from CSV 2 PDF
async def write2PDF():

    # Read data from CSV
    for filename in FILENAMES:
        pdf = fpdf.FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()
        pdf.add_font("IANSUI", "", "./Iansui-Regular.ttf")
        pdf.set_font("IANSUI", "", 10)  # Reduced font size
        with open(filename + ".csv", "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            data = list(csv_reader)

        # Set up table with adjusted column widths
        col_widths = [17, 17, 17]
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
        pdf.output(filename + ".pdf")


if __name__ == "__main__":
    run(init_csv())
    run(write2CSV())
    run(write2PDF())
