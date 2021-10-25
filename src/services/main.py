from data import callback_data_attrs as ca
from data.database import Student, Subscription, Manager, Subject, Month, Tariff
from services.gsheet import find_student, gc_add_new_user, gc_update_user


async def is_student_exist(email: str, subject_id: int):
    student = await Student.query.where(Student.email == email).gino.first()
    subscription = None
    if student:
        subscription = (
            await Subscription.query.where(Subscription.subject == subject_id)
            .where(Subscription.user == student.id)
            .gino.first()
        )
    if not subscription:
        row_values = await find_student(email, subject_id)
        if row_values:
            return row_values[0]
        return None
    return student.full_name


async def add_update_student(manager_id: int, state_data: dict):
    student = await Student.query.where(
        Student.email == state_data["email"],
    ).gino.first()
    manager = await Manager.get(manager_id)
    subject = await Subject.get(int(state_data[ca.SUBJECT]))
    tariff = await Tariff.get(int(state_data[ca.TARIFF]))
    if state_data[ca.MONTH] == "all_year":
        month = "all_year"
    else:
        month = await Month.get(int(state_data[ca.MONTH]))
    if not student:
        student = await Student.create(
            full_name=state_data["vk_name"],
            vk_url=state_data["vk_url"],
            email=state_data["email"],
        )
        await gc_add_new_user(student, manager, subject, month, tariff)
    else:
        try:
            await student.update(
                full_name=state_data["vk_name"],
                vk_url=state_data["vk_url"],
                email=state_data["email"],
            ).apply()
        except KeyError:
            pass
        await gc_update_user(student, manager, subject, month, tariff)
    if month == "all_year":
        months = await Month.query.gino.all()
        for month in months:
            subscription = (
                await Subscription.query.where(user=student.id)
                .where(tariff=int(state_data[ca.TARIFF]))
                .where(month=month.id)
                .where(subject=int(state_data[ca.SUBJECT]))
                .where(sale_type=int(state_data[ca.SALE_TYPE]))
                .gino.first()
            )
            if not subscription:
                await Subscription.create(
                    user=student.id,
                    tariff=int(state_data[ca.TARIFF]),
                    month=month.id,
                    subject=int(state_data[ca.SUBJECT]),
                    sale_type=int(state_data[ca.SALE_TYPE]),
                )
    else:
        subscription = (
            await Subscription.query.where(user=student.id)
            .where(tariff=int(state_data[ca.TARIFF]))
            .where(month=int(state_data[ca.MONTH]))
            .where(subject=int(state_data[ca.SUBJECT]))
            .where(sale_type=int(state_data[ca.SALE_TYPE]))
            .gino.first()
        )
        if not subscription:
            await Subscription.create(
                user=student.id,
                tariff=int(state_data[ca.TARIFF]),
                month=int(state_data[ca.MONTH]),
                subject=int(state_data[ca.SUBJECT]),
                sale_type=int(state_data[ca.SALE_TYPE]),
            )
