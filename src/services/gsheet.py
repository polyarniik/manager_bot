import os

import gspread
from google.oauth2.service_account import Credentials

from config.config import GOOGLE_SPREADSHEET_ID
from data.database import Student, Manager, Month, Subject, Tariff

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

credentials = Credentials.from_service_account_file(
    filename=os.path.abspath("data/credentials.json"), scopes=scopes
)

gc = gspread.authorize(credentials)
sh = gc.open_by_key(GOOGLE_SPREADSHEET_ID)


def __gc_next_available_row(worksheet) -> int:
    str_list = list(filter(None, worksheet.col_values(1)))
    if len(str_list) == worksheet.row_count:
        worksheet.resize(worksheet.row_count + 50)
    return len(str_list) + 1


def __gc_find_user(worksheet: gspread.models.Worksheet, email: str) -> int:
    for cell in worksheet.findall(email):
        return cell.row
    return -1


async def gc_add_new_user(
        student: Student, manager: Manager, subject: Subject, month, tariff: Tariff
):
    try:
        sheet = sh.worksheet(subject.name)
        row = __gc_next_available_row(sheet)
        sheet.update_cell(row, 1, student.full_name)
        sheet.update_cell(row, 2, student.vk_url)
        sheet.update_cell(row, 3, student.email)
        sheet.update_cell(row, 4, manager.full_name)
        if isinstance(month, Month):
            sheet.update_cell(row, 7, month.name)
            sheet.update_cell(row, month.column, tariff.name)
        else:
            months = await Month.query.gino.all()
            sheet.update_cell(row, 7, months[0].name)
            for month in months:
                sheet.update_cell(row, month.column, tariff.name)
    except gspread.exceptions.GSpreadException:
        return False
    return True


async def gc_update_user(
        student: Student,
        manager: Manager,
        subject: Subject,
        month,
        tariff: Tariff,
):
    try:
        sheet = sh.worksheet(subject.name)
        row = __gc_find_user(sheet, student.email)
        sheet.update_cell(row, 1, student.full_name)
        sheet.update_cell(row, 2, student.vk_url)
        sheet.update_cell(row, 3, student.email)
        sheet.update_cell(row, 4, manager.full_name)
        if isinstance(month, Month):
            sheet.update_cell(row, month.column, tariff.name)
        else:
            months = await Month.query.gino.all()
            for month in months:
                sheet.update_cell(row, month.column, tariff.name)
    except gspread.exceptions.GSpreadException as e:
        print(e)
        return False
    return True


async def find_student(email: str, subject_id: int):
    subject = await Subject.get(subject_id)
    print(sh.worksheets())
    sheet = sh.worksheet(subject.name)
    row = __gc_find_user(sheet, email)
    if row != -1:
        return sheet.row_values(row)
    return None
