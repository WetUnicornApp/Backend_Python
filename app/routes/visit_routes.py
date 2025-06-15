from flask import Blueprint

from app.models.animal_models.animal import Animal
from app.models.organization_models.employee import Employee
from app.models.owner_models.owner import Owner
from app.models.user_models.user_model import UserModel
from app.models.visit_models.visit_animal import VisitAnimal
from app.repositories.visits_repository.visit_animal_repository import VisitAnimalRepository
from datetime import datetime
from flask import Blueprint, request
from app.models.calendar_models.calendar import Calendar
from app.models.visit_models.visit import Visit
from app.models.visit_models.visit_employee import VisitEmployee
from app.repositories.calendar_repository import CalenderRepository
from app.repositories.visits_repository.visit_repository import VisitRepository
from app.repositories.visits_repository.visits_employee_repository import VisitEmployeeRepository
from app.utils.api_response import ApiResponse
from config.database import SessionLocal
from app.models.user_models.user import User

visit_bp = Blueprint('visit', __name__)


@visit_bp.route('/create', methods=['POST'])
def create_visit():
    session = SessionLocal()

    try:
        data = request.get_json()
        date_planned = data.get("date")
        time_planned = data.get("time")
        datetime_planned = datetime.strptime(f"{date_planned} {time_planned}", "%Y-%m-%d %H:%M")

        employee_id = data.get("employee_id")

        if employee_id:
            existing_visit_ids = session.query(VisitEmployee.visit_id).filter_by(employee_id=employee_id).all()
            visit_ids = [v[0] for v in existing_visit_ids]

            if visit_ids:
                conflicting = session.query(Visit).join(Calendar).filter(
                    Visit.id.in_(visit_ids),
                    Calendar.datetime_planned == datetime_planned
                ).first()

                if conflicting:
                    return ApiResponse(
                        f"EMPLOYEE_IS_OCCURRED",
                        False
                    ).return_response(), 400

        calendar_data = {
            "datetime_created": data.get("datetime_created", datetime.utcnow()),
            "datetime_planned": datetime_planned
        }
        calendar = Calendar(**calendar_data)
        calendar_repo = CalenderRepository(session)
        calendar_repo.create(calendar)
        session.flush()

        visit_data = {
            "name": data.get("name", ''),
            "description": data.get("description"),
            "calendar_id": calendar.id
        }
        visit = Visit(**visit_data)
        visit_repo = VisitRepository(session)
        visit_repo.create(visit)
        session.flush()

        employee_id = data.get("employee_id")
        visit_employee = None
        if employee_id:
            visit_employee = VisitEmployee(visit_id=visit.id, employee_id=employee_id)
            visit_employee_repo = VisitEmployeeRepository(session)
            visit_employee_repo.create(visit_employee)

        animal_id = data.get("pet_id")
        visit_animal = None
        if animal_id:
            visit_animal = VisitAnimal(visit_id=visit.id, animal_id=animal_id)
            visit_animal_repo = VisitAnimalRepository(session)
            visit_animal_repo.create(visit_animal)

        session.commit()

        response_data = {
            "calendar": calendar.to_dict(),
            "visit": visit.to_dict(),
            "visit_employee": visit_employee.to_dict() if visit_employee else None
        }

        return ApiResponse(response_data, True).return_response(), 200

    except Exception as e:
        session.rollback()
        return ApiResponse(f"Error creating visit: {str(e)}", False).return_response(), 400


@visit_bp.route('/edit/<int:visit_id>', methods=['PUT'])
def edit(visit_id):
    db = SessionLocal()

    try:
        data = request.get_json()

        visit = db.query(Visit).filter_by(id=visit_id).first()
        if not visit:
            return ApiResponse(f"Visit with ID {visit_id} does not exist.", False).return_response(), 404

        calendar = db.query(Calendar).filter_by(id=visit.calendar_id).first()
        if not calendar:
            return ApiResponse("Associated calendar not found.", False).return_response(), 404

        visit.name = data.get("name", visit.name)
        visit.description = data.get("description", visit.description)

        date_planned = data.get("date")
        time_planned = data.get("time")
        new_datetime = datetime.strptime(f"{date_planned} {time_planned}", "%Y-%m-%d %H:%M")

        if new_datetime:
            if isinstance(new_datetime, str):
                new_datetime = datetime.fromisoformat(new_datetime)

            employee_id = data.get("employee_id")
            if employee_id:
                existing_visit_ids = db.query(VisitEmployee.visit_id).filter_by(employee_id=employee_id).all()
                visit_ids = [v[0] for v in existing_visit_ids]

                if visit_ids:
                    conflicting = db.query(Visit).join(Calendar).filter(
                        Visit.id.in_(visit_ids),
                        Calendar.datetime_planned == new_datetime,
                        Visit.id != visit.id
                    ).first()

                    if conflicting:
                        return ApiResponse(
                            "EMPLOYEE_IS_OCCURRED",
                            False
                        ).return_response(), 400

            calendar.datetime_planned = new_datetime

        if "employee_id" in data:
            employee_id = data["employee_id"]
            visit_employee = db.query(VisitEmployee).filter_by(visit_id=visit.id).first()

            if visit_employee:
                visit_employee.employee_id = employee_id
            else:
                visit_employee = VisitEmployee(visit_id=visit.id, employee_id=employee_id)
                visit_employee_repo = VisitEmployeeRepository(db)
                visit_employee_repo.create(visit_employee)

        if "pet_id" in data:
            animal_id = data["pet_id"]
            visit_animal = db.query(VisitAnimal).filter_by(visit_id=visit.id).first()

            if visit_animal:
                visit_animal.animal_id = animal_id
            else:
                visit_animal = VisitAnimal(visit_id=visit.id, animal_id=animal_id)
                visit_animal_repo = VisitAnimalRepository(db)
                visit_animal_repo.create(visit_animal)

        db.commit()

        visit_employee = db.query(VisitEmployee).filter_by(visit_id=visit.id).first()
        visit_animal = db.query(VisitAnimal).filter_by(visit_id=visit.id).first()

        response = {
            "visit": visit.to_dict(),
            "calendar": calendar.to_dict(),
            "employee_id": visit_employee.employee_id if visit_employee else None,
            "animal_id": visit_animal.animal_id if visit_animal else None
        }

        return ApiResponse(response, True).return_response(), 200

    except Exception as e:
        db.rollback()
        return ApiResponse(f"Error editing the visit: {str(e)}", False).return_response(), 400


@visit_bp.route('/delete/<int:visit_id>', methods=['DELETE'])
def delete(visit_id):
    db = SessionLocal()

    try:
        repo = CalenderRepository(db)
        vist_repo = VisitRepository(db)
        visit_emp_rep = VisitEmployeeRepository(db)
        vist_animal_rep = VisitAnimalRepository(db)

        visit = db.query(Visit).filter_by(id=visit_id).first()
        if not visit:
            return ApiResponse(f"No visit associated with ID {visit_id}.", False).return_response(), 404

        calendar = db.query(Calendar).filter_by(id=visit.calendar_id).first()
        if not calendar:
            return ApiResponse(f"Calendar with ID {visit_id} does not exist.", False).return_response(), 404

        visit_emp = db.query(VisitEmployee).filter_by(visit_id=visit.id).first()

        visit_animal = db.query(VisitAnimal).filter_by(visit_id=visit.id).first()

        if visit_animal:
            vist_animal_rep.delete(visit_animal)

        if visit_emp:
            visit_emp_rep.delete(visit_emp)

        vist_repo.delete(visit)
        repo.delete(calendar)

        return ApiResponse("The visit and related data have been marked as deleted.", True).return_response(), 200


    except Exception as e:
        db.rollback()
        return ApiResponse(f"Error deleting the visit: {str(e)}", False).return_response(), 400


@visit_bp.route('/list', methods=['GET'])
def list():
    db = SessionLocal()

    try:
        visit_repo = VisitRepository(db)
        visits = db.query(Visit).filter_by(is_deleted=0).all()

        result = []

        for visit in visits:
            calendar = db.query(Calendar).filter_by(id=visit.calendar_id).first()
            visit_employee = db.query(VisitEmployee).filter_by(visit_id=visit.id).first()
            employee = db.query(Employee).filter_by(id=visit_employee.employee_id).first()
            user_e = db.query(User).filter_by(id=employee.user_id).first()

            visit_animal = db.query(VisitAnimal).filter_by(visit_id=visit.id).first()
            animal = db.query(Animal).filter_by(id=visit_animal.animal_id).first()
            owner = db.query(Owner).filter_by(id=animal.owner_id).first()
            user_o = db.query(User).filter_by(id=owner.user_id).first()
            result.append({
                'id': visit.id,
                "visit": visit.to_dict(),
                'employee_name': user_e.first_name + ' ' + user_e.last_name,
                'owner_name': user_o.first_name + ' ' + user_o.last_name,
                'pat_name': animal.name,
                'visit_name': visit.name,
                'visit_description': visit.description,
                'date': calendar.datetime_planned.strftime('%d.%m.%Y'),
                'time': calendar.datetime_planned.strftime("%H:%M"),
                "calendar": calendar.to_dict() if calendar else None,
                "employee_id": visit_employee.employee_id if visit_employee else None
            })

        return ApiResponse('OK', True, result).return_response(), 200

    except Exception as e:
        return ApiResponse(f"Error fetching visits: {str(e)}", False).return_response(), 400


@visit_bp.route('/view/<int:visit_id>', methods=['GET'])
def get_visit(visit_id):
    db = SessionLocal()

    try:
        visit = db.query(Visit).filter_by(id=visit_id).first()
        if not visit:
            return ApiResponse(f"Visit with ID {visit_id} does not exist.", False).return_response(), 404

        calendar = db.query(Calendar).filter_by(id=visit.calendar_id).first()
        visit_employee = db.query(VisitEmployee).filter_by(visit_id=visit.id).first()
        employee = db.query(Employee).filter_by(id=visit_employee.employee_id).first()
        user_e = db.query(User).filter_by(id=employee.user_id).first()

        visit_animal = db.query(VisitAnimal).filter_by(visit_id=visit.id).first()
        animal = db.query(Animal).filter_by(id=visit_animal.animal_id).first()
        owner = db.query(Owner).filter_by(id=animal.owner_id).first()
        user_o = db.query(User).filter_by(id=owner.user_id).first()
        result = {
            "name": visit.name,
            "description": visit.description,
            'date': calendar.datetime_planned.strftime('%Y-%m-%d'),
            'time': calendar.datetime_planned.strftime("%H:%M"),
            'employee': user_e.first_name + ' ' + user_e.last_name,
            'employee_id':employee.id,
            'owner': user_o.first_name + ' ' + user_o.last_name,
            'pet': animal.name,
            'pet_id': animal.id,
            'owner_id': owner.id,
            'id':visit.id,
        }

        return ApiResponse('OK', True, result).return_response(), 200

    except Exception as e:
        return ApiResponse(f"Error fetching visit: {str(e)}", False).return_response(), 400
